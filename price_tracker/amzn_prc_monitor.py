import asyncio
import os
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
from datetime import datetime
from pot_schema import pot
from product_schema import Log


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = Path("/home/syed/Downloads/Workspace/Scripts/profiles/syed")  # Mine was C:/Users/syedm/OneDrive/Desktop/Scripts/profiles/syed

async def main():
    with open(os.path.join(BASE_DIR, "products_list.json")) as f:
                data = json.load(f)

    with open(os.path.join(BASE_DIR, "price_over_time.json")) as f:
                pData= json.load(f)

    with open(os.path.join(BASE_DIR, "log.json")) as f:
                logD= json.load(f)

    potData= [pot(**item) for item in pData]
    product_list = [product(**item) for item in data]
    logData= [Log(**item) for item in logD]

    temp_list=product_list.copy()
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",        # use installed Chrome
            headless=True,          # It's better to see the browser in action or it might not work as expected due to not seeing the UI
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
        )
    

        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        for item in temp_list:
            try :
                await page.goto(item.url, timeout=60_000) 
                # await page.wait_for_selector("span.a-offscreen")
                # price_str = await page.locator("span.a-offscreen").first.text_content()
                
                await page.wait_for_selector("span.a-price span.a-offscreen",state="attached")
                price_str = await page.locator("span.a-price span.a-offscreen").first.text_content()
                price_str= str(price_str) if price_str is not None else ""
                price_formatted = float(price_str.replace("₹", "").replace(",", "").strip())

                potData.append(pot(uid=len(potData),product_id=item.pid,price=price_formatted,timestamp=datetime.now().isoformat()))
                if price_formatted<item.price:
                    log_msg=f"Price for {item.name} has dropped from {item.price} to {price_formatted}. Check the URL:{item.url}"
                    logData.append(Log(id=len(logData),name=item.name,last_price=item.price,new_price=price_formatted,url=item.url,log_msg=log_msg))

                    # print("Max Price is less",price_formatted)
                    for pr in product_list:
                        if pr.pid == item.pid:
                            pr.price=price_formatted 
                            pr.visual_price=price_str 

                            break

                    with open(os.path.join(BASE_DIR, "products_list.json"), "w") as f:
                        json.dump([asdict(p) for p in product_list], f, indent=2,   ensure_ascii=False)

                    with open(os.path.join(BASE_DIR, "log.json"), "w") as f:
                        json.dump([asdict(p) for p in logData], f, indent=2,   ensure_ascii=False)
                elif price_formatted>item.price:
                    log_msg=f"Price for {item.name} has increased from {item.price} to {price_formatted}. Check the URL:{item.url}"
                    logData.append(Log(id=len(logData),name=item.name,last_price=item.price,new_price=price_formatted,url=item.url,log_msg=log_msg))

                    with open(os.path.join(BASE_DIR, "log.json"), "w") as f:
                        json.dump([asdict(p) for p in logData], f, indent=2,   ensure_ascii=False)
                # else:print(f"\n Product Name {item.name} Product Price {item.price} is same\n ")




                with open(os.path.join(BASE_DIR, "price_over_time.json"), "w") as f:
                    json.dump([asdict(p) for p in potData], f, indent=2,   ensure_ascii=False)

            except Exception as e:
                print("This went wrong ",e)
            # await asyncio.sleep(1)  

        print(f"Run on {datetime.now()}")
        await ctx.close()
 
        
if __name__=="__main__":
    asyncio.run(main())
