import asyncio
import json
import os
from playwright.async_api import async_playwright
import datetime
import random

async def main():
    async with async_playwright() as p:
        # Launch with stealth settings to avoid detection
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )

        # Create context with realistic user agent
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        site_name = "naukri"  # Change this for different sites
        cookie_file = rf'C:\Users\syedm\OneDrive\Desktop\MyScripts\{site_name}_cookies.json'

        # Load existing cookies if available
        if os.path.exists(cookie_file):
            print(f"Loading saved {site_name} cookies...")
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)

        page = await context.new_page()

        # Remove automation indicators
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        await page.goto('https://www.naukri.com/mnjuser/profile?id=&altresid')

        # Wait for the file input to appear (triggered by JS when page loads)
        file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)

        # Upload your resume directly (no file explorer)
        resume_files = [
            rf"C:\Users\syedm\Downloads\Syed_NCV.pdf",
            rf"C:\Users\syedm\Downloads\Syed_SE.pdf"
        ]
        resume_path = random.choice(resume_files)
        print(f"Randomly selected resume for upload: {resume_path}")
        log_path = rf"C:\Users\syedm\OneDrive\Desktop\MyScripts\log.txt"
        status = ""
        try:
            await file_input.set_input_files(resume_path)
            # Trigger the change event on the file input
            await page.evaluate('(input) => input.dispatchEvent(new Event("change", { bubbles: true }))', file_input)
            print("File uploaded and change event triggered!")
            status = "SUCCESS"
        except Exception as e:
            print(f"File upload failed: {e}")
            status = f"FAILED: {e}"

        # Log the result
        with open(log_path, "a") as logf:
            dt_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            logf.write(f"{dt_str} - Resume upload: {status}\n")

        print("Waiting 5 seconds before closing browser...")
        await asyncio.sleep(3)
        print("Closing browser...")
        await browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())