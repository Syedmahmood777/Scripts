import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
import datetime
import random

PROFILE_DIR = Path("C:/Users/syedm/OneDrive/Desktop/MyScripts/profiles/syed")
async def main():
     async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",        # use installed Chrome
            headless=False,          # It's better to see the browser in action or it might not work as expected due to not seeing the UI
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"]
        )
    
    
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        await page.goto("https://www.naukri.com/mnjuser/profile?id=&altresid", timeout=60_000)

        file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)
        resume_files = [
            rf"C:\Users\syedm\Downloads\Syed_NCV.pdf",
            rf"C:\Users\syedm\Downloads\Syed_SE.pdf"
        ]

        resume_path = random.choice(resume_files)
      
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

       
        await asyncio.sleep(1)      
        await ctx.close()
          


if __name__ == "__main__":
    asyncio.run(main())