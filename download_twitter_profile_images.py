import re
import os
import sys
import time
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
    return line  # If no @ or URL pattern found, assume it's just the username

def get_profile_image_url(username):
    url = f"https://x.com/{username}"
    _xhr_calls = []
    
    def intercept_response(response):
        """capture all background requests and save them"""
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # enable background request intercepting:
        page.on("response", intercept_response)
        
        try:
            # go to url and wait for the page to load with a longer timeout (30s)
            page.goto(url, wait_until="networkidle", timeout=30000)
            # Wait for the primary column to load
            page.wait_for_selector("[data-testid='primaryColumn']", timeout=30000)
            
            # Try multiple ways to get the profile image
            
            # Method 1: Check UserBy API calls
            user_calls = [f for f in _xhr_calls if "UserBy" in f.url]
            for xhr in user_calls:
                try:
                    data = xhr.json()
                    if 'data' in data and 'user' in data['data'] and 'result' in data['data']['user']:
                        user_data = data['data']['user']['result']
                        if 'legacy' in user_data and 'profile_image_url_https' in user_data['legacy']:
                            profile_img_url = user_data['legacy']['profile_image_url_https']
                            # Get original size by removing _normal or other size indicators
                            profile_img_url = re.sub(r"_(?:normal|bigger|mini)(\.\w+)$", r"\1", profile_img_url)
                            return profile_img_url
                except Exception as e:
                    print(f"Error parsing UserBy API data: {e}")
                    continue
            
            # Method 2: Try to extract directly from the page
            try:
                # Wait for the avatar to appear
                page.wait_for_selector('a[href$="/photo"] img[src*="profile_images"]', timeout=10000)
                avatar_img = page.query_selector('a[href$="/photo"] img[src*="profile_images"]')
                if avatar_img:
                    img_src = avatar_img.get_attribute('src')
                    if img_src:
                        # Get original size by removing _normal or other size indicators
                        profile_img_url = re.sub(r"_(?:normal|bigger|mini)(\.\w+)$", r"\1", img_src)
                        return profile_img_url
            except Exception as e:
                print(f"Error extracting image from page HTML: {e}")
                pass
            
            # Method 3: Look for any image that seems to be a profile image in the page
            try:
                imgs = page.query_selector_all('img[src*="profile_images"]')
                if imgs and len(imgs) > 0:
                    for img in imgs:
                        img_src = img.get_attribute('src')
                        if img_src and 'profile_images' in img_src:
                            # Get original size by removing _normal or other size indicators
                            profile_img_url = re.sub(r"_(?:normal|bigger|mini)(\.\w+)$", r"\1", img_src)
                            return profile_img_url
            except Exception as e:
                print(f"Error extracting alternate images: {e}")
                pass
            
            return None
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            return None

def download_image(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
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
            print(f"Found image URL: {img_url}")
            img = download_image(img_url)
            img_circ = crop_to_circle(img)
            out_path = os.path.join('profile_images', f'{username}.png')
            img_circ.save(out_path)
            print(f"Saved {out_path}")
            # Add a small delay between requests to avoid rate limiting
            time.sleep(1)
        except Exception as e:
            print(f"Failed for {username}: {e}")

if __name__ == "__main__":
    main()
