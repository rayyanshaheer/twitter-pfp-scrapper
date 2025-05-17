import re
import os
import sys
from io import BytesIO
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
import requests

def parse_username(line):
    line = line.strip()
    if not line:
        return None
    if line.startswith('@'):
        return line[1:]
    # Try to extract username from URL
    m = re.search(r"twitter.com/([A-Za-z0-9_]+)", line)
    if m:
        return m.group(1)
    m = re.search(r"x.com/([A-Za-z0-9_]+)", line)
    if m:
        return m.group(1)
    return None

def get_profile_image_url(username):
    url = f"https://x.com/{username}"
    _xhr_calls = []
    def intercept_response(response):
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.on("response", intercept_response)
        page.goto(url)
        page.wait_for_selector("[data-testid='primaryColumn']", timeout=15000)
        user_calls = [f for f in _xhr_calls if "UserBy" in f.url]
        for xhr in user_calls:
            data = xhr.json()
            try:
                profile_img_url = data['data']['user']['result']['legacy']['profile_image_url_https']
                # Get original size
                profile_img_url = profile_img_url.replace('_normal', '')
                return profile_img_url
            except Exception:
                continue
    return None

def download_image(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content)).convert("RGBA")

def crop_to_circle(im):
    size = min(im.size)
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    im = im.resize((size, size), Image.LANCZOS)
    output.paste(im, (0, 0), mask)
    return output

def main():
    if not os.path.exists('usernames.txt'):
        print('usernames.txt not found!')
        sys.exit(1)
    with open('usernames.txt', 'r', encoding='utf-8') as f:
        usernames = [parse_username(line) for line in f]
    usernames = [u for u in usernames if u]
    os.makedirs('profile_images', exist_ok=True)
    for username in usernames:
        print(f"Processing {username}...")
        img_url = get_profile_image_url(username)
        if not img_url:
            print(f"Could not find profile image for {username}")
            continue
        try:
            img = download_image(img_url)
            img_circ = crop_to_circle(img)
            out_path = os.path.join('profile_images', f'{username}.png')
            img_circ.save(out_path)
            print(f"Saved {out_path}")
        except Exception as e:
            print(f"Failed for {username}: {e}")

if __name__ == "__main__":
    main()
