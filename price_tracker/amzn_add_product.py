import asyncio
import traceback
import json
from pathlib import Path
from playwright.async_api import async_playwright
import datetime
import random
from product_schema import product 
from typing import List
import sys
from pathlib import Path
from dataclasses import asdict
from pot_schema import pot
from datetime import datetime
PROFILE_DIR = Path("/home/syed/Downloads/Workspace/Scripts/profiles/syed")  # Mine was C:/Users/syedm/OneDrive/Desktop/Scripts/profiles/syed

async def main():
    
    if len(sys.argv) == 3:
        product_name= sys.argv[1]
        product_url= sys.argv[2]
    else: 
        product_url="nothing"
        print("fix your arguments,pal")
        return
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",        # use installed Chrome
            headless=False,          # It's better to see the browser in action or it might not work as expected due to not seeing the UI
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
        )
    
        try :
            page = ctx.pages[0] if ctx.pages else await ctx.new_page()

            await page.goto(product_url, timeout=60_000) 

            await page.wait_for_selector("span.a-price span.a-offscreen",state="attached")
            price_str = await page.locator("span.a-price span.a-offscreen").first.text_content()
            price_str= str(price_str) if price_str is not None else ""
            price_formatted = float(price_str.replace("₹", "").replace(",", "").strip())
            print(f"\n Product Name {product_name} Product Price {price_str}\n ")
            with open("products_list.json") as f:
                data = json.load(f)

            with open("price_over_time.json") as f:
                pData= json.load(f)

            product_list = [product(**item) for item in data]
            pid=len(product_list)
            product_list.append(product(
                pid=pid,
                name=product_name,
                visual_price=price_str,
                price=price_formatted,
                url=product_url
               ))

            potData= [pot(**item) for item in pData]
            now=datetime.now()
            potData.append(pot(uid=len(potData),product_id=pid,price=price_formatted,timestamp=now.isoformat()))
            with open("products_list.json", "w") as f:
                json.dump([asdict(p) for p in product_list], f, indent=2,   ensure_ascii=False)

            with open("price_over_time.json", "w") as f:
                json.dump([asdict(p) for p in potData], f, indent=2,   ensure_ascii=False,)

            print("Worked")
        except Exception as e:
            print("This went wrong ",e)
            traceback.print_exc()
        # await asyncio.sleep(1)      
        await ctx.close()
 
        
if __name__=="__main__":
    asyncio.run(main())
