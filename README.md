# Twitter Profile Image Bulk Downloader

This project downloads Twitter (X.com) profile images in bulk using a list of usernames or profile URLs, then crops each image into a rounded transparent PNG. It is suitable for both developers and end-users.

---

## For Developers (Linux/Windows/Mac)

### Features
- Bulk download Twitter profile images using Playwright (headless browser)
- Accepts usernames in `@username` or full URL format
- Crops images into circular PNGs with transparency using Pillow
- Saves results in a `profile_images/` folder

### Requirements
- Python 3.8+
- pip (Python package manager)

### Setup
1. **Clone or copy the project files**
2. **Install dependencies:**
   ```bash
   pip install playwright pillow requests
   python -m playwright install
   # On Linux, also run:
   python -m playwright install-deps
   ```
3. **Prepare your usernames file:**
   - Edit `usernames.txt` and add one username or profile URL per line (e.g. `@jack` or `https://twitter.com/jack`).

4. **Run the script:**
   ```bash
   python download_twitter_profile_images.py
   ```
   - On some systems, use `python3` instead of `python`.

5. **Results:**
   - Cropped PNGs will be saved in the `profile_images/` folder.

---

## For Clients (Windows Users)

### What this does
- Downloads Twitter profile pictures for a list of usernames you provide
- Makes each image round and transparent (PNG)
- Saves all images in a folder called `profile_images`

### How to use
1. **Install Python**
   - Download and install Python 3.10+ from [python.org](https://www.python.org/downloads/)
   - During install, check "Add Python to PATH"

2. **Download project files**
   - Place `download_twitter_profile_images.py` and `usernames.txt` in the same folder

3. **Install requirements**
   - Open Command Prompt in the project folder
   - Run:
     ```cmd
     pip install playwright pillow requests
     python -m playwright install
     ```

4. **Edit `usernames.txt`**
   - Add one Twitter username per line (with or without @), or paste the full profile URL

5. **Run the script**
   - In Command Prompt, run:
     ```cmd
     python download_twitter_profile_images.py
     ```

6. **Find your images**
   - The images will appear in the `profile_images` folder, each as a round PNG

### Troubleshooting
- If you see errors about missing dependencies, make sure you installed everything in step 3
- If you see errors about Playwright or browsers, try running:
  ```cmd
  python -m playwright install
  ```

---

**Enjoy your bulk Twitter profile image downloader!**
