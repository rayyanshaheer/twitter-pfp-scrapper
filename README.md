# Twitter Profile Image Downloader

This script allows you to download Twitter/X profile images in bulk and convert them to circular transparent PNGs.

## Requirements

- Windows OS
- Python 3.6 or higher
- Internet connection

## How to Use

### Easy Method (For Windows Users)

1. Double-click the `run_twitter_downloader.bat` file.
2. The script will check if Python is installed and install required packages if needed.
3. Choose from the menu options:
   - Option 1: Use the default usernames.txt file
   - Option 2: Specify your own input file
   - Option 3: Exit

### Manual Method

1. Create a text file with Twitter/X usernames, one per line. Each line can be in any of these formats:
   - `@username`
   - `username`
   - `https://twitter.com/username`
   - `https://x.com/username`

2. Run the script from the command line:
   ```
   python twitter_profile_downloader.py path_to_usernames.txt --output output_folder_name
   ```

## Output

The script will create two files for each username:
- `username_original.jpg`: The original downloaded image
- `username_circular.png`: The image cropped into a circle with a transparent background

All output files will be saved to the specified output folder (default: "output").

## Notes

- This script does not use the official Twitter/X API, so it might stop working if Twitter changes their website structure.
- Please use this script responsibly and respect Twitter/X's terms of service.
- Processing many usernames might take some time depending on your internet connection.
