"""Snapshot the latest @nationalhumane Instagram posts for the prototype.

This stands in for what the WordPress site will do on its server: ask the
Instagram Graph API for the latest posts, keep the access token private, and
serve the result. Run it, then `python build.py`:

    PowerShell:  $env:NHS_IG_TOKEN = "<token>"; python fetch_instagram.py
    bash:        NHS_IG_TOKEN="<token>" python fetch_instagram.py

The token is read from the NHS_IG_TOKEN environment variable only. It is never
written to disk, printed or committed. The output is public post data only:
instagram_feed.json (permalink, type, caption, date, image file) and the
post images in assets/img/ig/, plus the profile picture (assets/img/ig-profile.jpg).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
OUT_JSON = HERE / "instagram_feed.json"
IMG_DIR = HERE / "assets" / "img" / "ig"

IG_ACCOUNT_ID = "17841402395422622"   # @nationalhumane (Instagram business account)
API = f"https://graph.facebook.com/v21.0/{IG_ACCOUNT_ID}/media"
LIMIT = 12
# Posts the current site hides from its feed (from its page code)
SKIP_SHORTCODES = ["DYyRDFFPAb1", "DaNyXJDIhr-"]


def fail(message, token=""):
    if token:
        message = message.replace(token, "[token]")
    sys.exit("fetch_instagram: " + message)


def main():
    token = os.environ.get("NHS_IG_TOKEN", "").strip()
    if not token:
        fail("set the NHS_IG_TOKEN environment variable first (see the top of this file).")

    query = urllib.parse.urlencode({
        "fields": "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp",
        "limit": LIMIT + len(SKIP_SHORTCODES),
        "access_token": token,
    })
    try:
        with urllib.request.urlopen(f"{API}?{query}", timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        fail(f"Instagram API error {e.code}: {detail}", token)
    except urllib.error.URLError as e:
        fail(f"could not reach the Instagram API: {e.reason}", token)

    posts = []
    for item in data.get("data", []):
        permalink = item.get("permalink", "")
        m = re.search(r"/(p|reel|tv)/([A-Za-z0-9_-]+)", permalink)
        if not m or m.group(2) in SKIP_SHORTCODES:
            continue
        image_url = item.get("thumbnail_url") if item.get("media_type") == "VIDEO" else item.get("media_url")
        if not image_url:
            continue
        posts.append({
            "id": item["id"],
            "kind": m.group(1),
            "shortcode": m.group(2),
            "permalink": permalink,
            "media_type": item.get("media_type"),
            "caption": (item.get("caption") or "").strip(),
            "timestamp": item.get("timestamp"),
            "image_url": image_url,
        })
        if len(posts) == LIMIT:
            break

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    keep = set()
    for post in posts:
        name = f"{post['id']}.jpg"
        keep.add(name)
        req = urllib.request.Request(post.pop("image_url"), headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            (IMG_DIR / name).write_bytes(resp.read())
        post["image"] = f"assets/img/ig/{name}"
    for old in IMG_DIR.glob("*.jpg"):
        if old.name not in keep:
            old.unlink()

    # The account's current profile picture, full size, for the avatar
    try:
        q = urllib.parse.urlencode({"fields": "profile_picture_url", "access_token": token})
        with urllib.request.urlopen(f"https://graph.facebook.com/v21.0/{IG_ACCOUNT_ID}?{q}", timeout=30) as resp:
            pic = json.load(resp).get("profile_picture_url")
        if pic:
            req = urllib.request.Request(pic, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                (HERE / "assets" / "img" / "ig-profile.jpg").write_bytes(resp.read())
    except (urllib.error.URLError, ValueError):
        print("Note: could not update the profile picture; keeping the current one.")

    OUT_JSON.write_text(json.dumps({"posts": posts}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    videos = sum(1 for p in posts if p["media_type"] == "VIDEO")
    print(f"Saved {len(posts)} posts ({videos} videos) to {OUT_JSON.name} and {IMG_DIR.relative_to(HERE)}/. Now run: python build.py")


if __name__ == "__main__":
    main()
