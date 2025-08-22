# persistent_profiles.py
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path("./profiles")

async def choose_profile() -> str:
    """Ask user to select or create a profile if not given."""
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    profiles = [p.name for p in BASE_DIR.iterdir() if p.is_dir()]

    if not profiles:
        print("No profiles found. Let's create a new one.")
        return input("Enter new profile name: ").strip()

    print("\nAvailable profiles:")
    for i, name in enumerate(profiles, 1):
        print(f"{i}. {name}")
    print(f"{len(profiles) + 1}. Create new profile")

    choice = input("Choose a profile number: ").strip()
    try:
        choice = int(choice)
        if 1 <= choice <= len(profiles):
            return profiles[choice - 1]
        elif choice == len(profiles) + 1:
            return input("Enter new profile name: ").strip()
    except ValueError:
        pass

    print("Invalid choice, defaulting to 'default'")
    return "default"

async def main():
    if len(sys.argv) >= 3:
        profile_name = sys.argv[1]
        site_url = sys.argv[2]
    elif len(sys.argv) == 2:
        profile_name = sys.argv[1]
        site_url = input("Enter site URL: ").strip()
    else:
        profile_name = await choose_profile()
        site_url = input("Enter site URL: ").strip()

    PROFILE_DIR = BASE_DIR / profile_name
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",        # use installed Chrome
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"]
        )

        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        print(f"\n🌐 Opening {site_url} with profile '{profile_name}'...")
        await page.goto(site_url, timeout=60_000)

        print("👉 Browser will stay open until you close it.")
        await page.wait_for_event("close")
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(main())
