import os
import re
import argparse
import requests
from PIL import Image, ImageDraw
import concurrent.futures
from urllib.parse import urlparse

def extract_username(text):
    """Extract Twitter/X username from either @username format or URL."""
    # Check if it's a URL
    if "twitter.com/" in text or "x.com/" in text:
        parsed_url = urlparse(text)
        path_parts = parsed_url.path.strip('/').split('/')
        if path_parts:
            return path_parts[0]
    # Check if it's in @username format
    elif text.startswith('@'):
        return text[1:]
    # It's just the username
    else:
        return text

def get_profile_image(username):
    """Get profile image URL for a given Twitter/X username."""
    try:
        # Use nitter.net as an alternative Twitter frontend that's easier to scrape
        # We'll try multiple nitter instances in case some are down
        nitter_instances = [
            f"https://nitter.net/{username}/pic",
            f"https://nitter.lacontrevoie.fr/{username}/pic",
            f"https://nitter.1d4.us/{username}/pic",
            f"https://nitter.kavin.rocks/{username}/pic",
            f"https://nitter.fly.dev/{username}/pic"
        ]
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://nitter.net/",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache"
        }
        
        for instance_url in nitter_instances:
            try:
                print(f"Trying to fetch profile image for {username} from {instance_url}")
                response = requests.get(instance_url, headers=headers, allow_redirects=True, timeout=10)
                response.raise_for_status()
                
                # If we get redirected to the actual image
                if response.url.startswith("https://pbs.twimg.com/profile_images/"):
                    img_url = re.sub(r'_(normal|bigger|mini|400x400)', '', response.url)
                    return img_url
                
                # Otherwise look for profile image in the HTML
                img_pattern = re.compile(r'(https://pbs.twimg.com/profile_images/[^"\'?\s]+)')
                matches = img_pattern.findall(response.text)
                
                if matches:
                    # Get the highest quality version by removing _normal, _bigger, etc.
                    img_url = re.sub(r'_(normal|bigger|mini|400x400)', '', matches[0])
                    return img_url
            
            except (requests.RequestException, Exception) as e:
                print(f"Error with {instance_url}: {str(e)}")
                continue
        
        # If we've tried all instances and still no luck, try using the twimg CDN directly
        try:
            # Twitter's CDN often uses a predictable URL pattern for profile images
            direct_url = f"https://pbs.twimg.com/profile_images/{username}/profile_image.jpg"
            response = requests.head(direct_url, headers=headers, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                return direct_url
        except Exception:
            pass
            
        print(f"Could not find profile image for {username}")
        return None
    
    except Exception as e:
        print(f"Error fetching profile for {username}: {e}")
        return None

def download_image(username, output_folder):
    """Download the profile image for a username."""
    img_url = get_profile_image(username)
    if not img_url:
        # As a fallback, try with a generic avatar service
        print(f"Trying alternative avatar service for {username}")
        img_url = f"https://unavatar.io/twitter/{username}"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Referer": "https://twitter.com/",
        }
        response = requests.get(img_url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()
        
        # Determine the extension from content-type or URL
        content_type = response.headers.get('content-type', '')
        ext = '.jpg'  # default
        
        if 'image/png' in content_type:
            ext = '.png'
        elif 'image/gif' in content_type:
            ext = '.gif'
        elif 'image/webp' in content_type:
            ext = '.webp'
        elif 'image/jpeg' in content_type or 'image/jpg' in content_type:
            ext = '.jpg'
        
        # Generate output filename
        output_path = os.path.join(output_folder, f"{username}_original{ext}")
        
        # Save the image
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded profile image for {username}")
        return output_path
    
    except requests.RequestException as e:
        print(f"Error downloading image for {username}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error downloading image for {username}: {e}")
        return False

def create_circular_mask(image):
    """Create a circular mask for the image."""
    width, height = image.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    return mask

def crop_to_circle(image_path, output_folder, username):
    """Crop an image to a circle with transparent background."""
    try:
        img = Image.open(image_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create mask
        mask = create_circular_mask(img)
        
        # Apply the mask
        new_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
        new_img.paste(img, (0, 0), mask)
        
        # Save the result
        output_path = os.path.join(output_folder, f"{username}_circular.png")
        new_img.save(output_path, format="PNG")
        
        print(f"Created circular image for {username}")
        return output_path
    
    except Exception as e:
        print(f"Error creating circular image for {username}: {e}")
        return False

def process_username(username, output_folder):
    """Process a single username."""
    clean_username = extract_username(username.strip())
    if not clean_username:
        print(f"Invalid username: {username}")
        return
    
    # Download image
    image_path = download_image(clean_username, output_folder)
    if not image_path:
        return
    
    # Crop to circle
    crop_to_circle(image_path, output_folder, clean_username)

def main():
    parser = argparse.ArgumentParser(description="Download Twitter/X profile images and crop them into circles")
    parser.add_argument("input_file", help="Text file with Twitter/X usernames (one per line)")
    parser.add_argument("--output", "-o", default="output", help="Output folder for images")
    parser.add_argument("--workers", "-w", type=int, default=3, help="Number of concurrent workers (default: 3)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")
    args = parser.parse_args()
    
    print("Twitter Profile Image Downloader")
    print("=" * 30)
    
    # Create output directory if it doesn't exist
    try:
        os.makedirs(args.output, exist_ok=True)
        print(f"Output directory: {os.path.abspath(args.output)}")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        return
    
    # Read usernames from file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"Found {len(usernames)} usernames in {args.input_file}")
    except Exception as e:
        print(f"Error reading input file: {e}")
        print("Make sure the file exists and is readable")
        return
    
    if not usernames:
        print("No usernames found in the input file. Please add usernames to the file and try again.")
        return
    
    print(f"\nProcessing {len(usernames)} usernames with {args.workers} worker threads...")
    print("This might take some time depending on your internet connection.")
    print("=" * 30)
    
    # Create a counter for successful downloads
    successful = 0
    
    # Process usernames in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(process_username, username, args.output) for username in usernames]
        
        # Count successful downloads
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                successful += 1
    
    # Check the output directory
    try:
        created_files = [f for f in os.listdir(args.output) if os.path.isfile(os.path.join(args.output, f))]
        circular_images = [f for f in created_files if f.endswith('_circular.png')]
        
        print("\nSummary:")
        print(f"Successfully processed: {successful} out of {len(usernames)} usernames")
        print(f"Created {len(circular_images)} circular transparent PNG images")
        print(f"All files are saved in: {os.path.abspath(args.output)}")
        
        if not circular_images:
            print("\nWarning: No circular images were created. Check the error messages above.")
    except Exception as e:
        print(f"Error checking output directory: {e}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
