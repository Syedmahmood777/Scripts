import asyncio
import json
import os
from playwright.async_api import async_playwright

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
        
        site_name = "linkedin"  # Change this for different sites
        cookie_file = f'{site_name}_cookies.json'
        
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
        
        await page.goto('https://www.linkedin.com')  # Change to any site you want

        if os.path.exists(cookie_file):
            print("Using saved session!")
        else:
            print("Login manually in the browser window.")
            print("If you are logging in with Google, complete all popups and redirects.")
            print("If a Google login popup appears, do NOT close it. Complete the login in the popup window.")

            popup = None
            def handle_popup(p):
                nonlocal popup
                popup = p
                print("Google login popup detected. Please complete the login in the popup window.")
            page.once("popup", handle_popup)

            input("Press Enter here in the terminal after you see your LinkedIn feed (main window)...")

            # If popup was opened, wait for it to close (user finished Google login)
            if popup:
                print("Waiting for Google login popup to close...")
                try:
                    await popup.wait_for_event('close', timeout=120_000)
                except Exception:
                    print("Popup did not close in time, continuing anyway.")
        
        # Save only cookies for this specific site
        site_cookies = await context.cookies('https://www.linkedin.com')
        with open(cookie_file, 'w') as f:
            json.dump(site_cookies, f)
        print(f"Saved {len(site_cookies)} cookies for {site_name}!")
        
        
        # Keep browser open until you close it manually
        print("Browser will stay open until you close it manually...")
        try:
            await page.wait_for_event('close')
        except:
            pass


if __name__ == "__main__":
    asyncio.run(main())