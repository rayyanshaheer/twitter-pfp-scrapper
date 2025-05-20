# Twitter/X Profile Image Bulk Downloader

This tool downloads Twitter (X.com) profile images in bulk using a list of usernames or profile URLs, then crops each image into a rounded transparent PNG. It uses advanced scraping techniques to retrieve profile images even with recent Twitter API limitations.

## Features

- **✅ Bulk Download**: Process multiple Twitter profiles at once
- **✅ Multiple Extraction Methods**: Uses three different approaches to find profile images
- **✅ Format Flexibility**: Accepts usernames as `@username`, plain username, or full profile URLs
- **✅ High Quality Images**: Retrieves full-size profile images (not thumbnails)
- **✅ Beautiful Output**: Crops images into perfectly circular PNGs with transparency
- **✅ Modern Web Scraping**: Uses Playwright for headless browser automation
- **✅ Error Handling**: Robust error handling with detailed logging
- **✅ Cross Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.8 or newer
- pip (Python package manager)

### Setup

1. **Clone or download this repository**

2. **Install dependencies:**

   ```bash
   pip install playwright pillow requests
   python -m playwright install
   ```

   On Linux, you may also need to install browser dependencies:

   ```bash
   python -m playwright install-deps
   ```

## Usage

1. **Prepare your usernames list:**
   
   Edit `usernames.txt` and add one username or profile URL per line in any of these formats:
   
   ```
   @elonmusk
   jack
   https://twitter.com/karpathy
   https://x.com/lexfridman
   ```

2. **Run the script:**

   ```bash
   python download_twitter_profile_images.py
   ```
   
   On some systems, use `python3` instead of `python`.

3. **Find your images:**
   
   The cropped profile images will be saved in the `profile_images/` directory as transparent PNGs.

## How It Works

This tool uses advanced web scraping techniques to:

1. Launch a headless browser using Playwright
2. Visit each Twitter profile page
3. Intercept XHR requests that contain profile data
4. Extract profile image URLs using multiple fallback methods
5. Download the highest quality images available
6. Process and crop images into perfect circles with transparency

## Troubleshooting

- **Twitter Layout Changes**: If the script stops working, it may be due to Twitter changing their page layout. Create an issue on GitHub for assistance.
- **Rate Limiting**: If processing many profiles at once, you might encounter rate limiting. The script includes a delay to help prevent this.
- **Browser Issues**: If you encounter browser-related errors, try reinstalling the Playwright browsers:
  ```bash
  python -m playwright install --force
  ```

## For Developers

The code is well-commented and modular. Key functions:

- `parse_username()`: Extracts usernames from various formats
- `get_profile_image_url()`: The core function that retrieves profile image URLs using multiple methods
- `crop_to_circle()`: Processes images into circular PNGs with transparency

Feel free to modify and extend this tool for your specific needs.

## License

This project is released under the MIT License.

## Acknowledgments

- Built with [Playwright](https://playwright.dev/) for browser automation
- Image processing with [Pillow](https://python-pillow.org/)
- Inspired by techniques from [ScrapFly](https://scrapfly.io/blog/how-to-scrape-twitter/)

---

**Last Updated**: May 2025
