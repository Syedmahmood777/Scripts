# Cookie Collector

A Python automation toolkit for managing browser sessions and automating various website interactions using Playwright/Selenium.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Available Modules](#available-modules)
  - [Update Resume on Naukri](#update-resume-on-naukri)
- [General Usage](#general-usage)
- [Module-Specific Instructions](#module-specific-instructions)
  - [Naukri Resume Update](#naukri-resume-update)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Coming Soon](#coming-soon)

## Requirements

- Python 3.7+
- Playwright
- Chrome browser
- Internet connection

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
python -m playwright install
```

## Available Modules

### Update Resume on Naukri
Automatically updates your resume on Naukri.com at scheduled intervals to improve visibility and ranking.

**Status:** ✅ Available

## General Usage

Cookie Collector saves all your browser sessions, so automation doesn't require you to log in every time it runs. This makes the process seamless and efficient.

### Initial Setup

1. **Create Browser Profile**: You must log in to all accounts you want to use on every website. Your session data will be saved under `.profiles` directory using the profile name you specify.

2. **Run the Cookie Collector**:
```bash
python cookie_collector.py your_profile_name https://www.naukri.com
```

3. **Login Process**: After running the script, log in to your account through the automated browser window then close the window once logged in.

## Module-Specific Instructions

### Naukri Resume Update

#### Setup Instructions

1. **Get Your Profile URL**:
   - Go to your Naukri profile
   - Navigate to the page where you can see your profile and the "Update Resume" button
   - Copy the complete URL from the address bar

2. **Configure the Script**:
   Open `update_naukri.py` and update the following 4 fields:

```python
# 1. Profile Directory Path
PROFILE_DIR = Path("YOUR_ABSOLUTE_PROFILE_PATH_HERE")

# 2. Your Naukri Profile URL
await page.goto("https://www.naukri.com/mnjuser/profile?id=&altresid", timeout=60_000)
# Replace with the profile URL you copied from your Naukri profile

# 3. Resume File Paths
resume_files = [
    rf"C:\Users\syedm\Downloads\Syed_NCV.pdf",
    rf"C:\Users\syedm\Downloads\Syed_SE.pdf"
]
# Add your resume paths here. You can have multiple resumes to choose from,
# or just keep one path in the list

# 4. Log File Path
log_path = rf"C:\Users\syedm\OneDrive\Desktop\Scripts\log.txt"
# Path to your log file. Should be in the same folder as the script.
# Copy the path to your root folder and add 'log.txt' at the end
```

> **Important**: Make sure all paths are absolute (full paths) rather than relative paths.

## Testing

### Test Naukri Resume Update

Run the following command to test the Naukri module:

```bash
python update_naukri.py
```

## Troubleshooting

- **Login Issues**: If you're prompted to log in repeatedly, ensure your profile was saved correctly during the initial setup
- **Path Errors**: Double-check that all file paths are absolute and the files exist
- **Browser Issues**: Make sure Chrome is installed and up to date
- **Network Issues**: Ensure stable internet connection during automation

## Coming Soon

- **LinkedIn Job Scrape** 🔄
- **Job Classifier** 🔄


---

## License

This project is for educational and personal use only. Please respect the terms of service of the websites you're automating.

---

**Note**: Always ensure you comply with the terms of service of the websites you're automating. This tool is intended for legitimate personal use only.