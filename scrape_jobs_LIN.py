import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright
import pandas as pd
import json
PROFILES_DIR = Path("./profiles")

async def click_jobs(job_containers, page):
    # job_containers is already a list of ElementHandles
    for job in job_containers:
        await job.scroll_into_view_if_needed()
        await job.click()
        await page.wait_for_timeout(500)  # small delay if needed

async def main():
    if len(sys.argv) < 3:
        print('''Usage: python scrape_jobs_LIN.py syed "https://www.linkedin.com/jobs/search/?currentJobId=4290642339&distance=25&f_E=2%2C3&geoId=102713980&keywords=data&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true" ''')
        sys.exit(1)

    profile_name = sys.argv[1]
    site_url = sys.argv[2]

    profile_path = PROFILES_DIR / profile_name
    profile_path.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            str(profile_path),
            channel="chrome",
            headless=False,
        )

        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        await page.goto(site_url, timeout=60_000)

            
        jobs = await page.evaluate(r"""
    (async () => {
    const processCurrentPage = async () => {
        const cont = document.getElementsByClassName('scaffold-layout__list')[0]?.children?.[1];
        if (!cont) return [];

        const seen = new Set();
        const results = [];
        const getCards = () => [...cont.getElementsByClassName('job-card-container--clickable'), 
                                ...cont.getElementsByTagName('job-card-container')];
        const getId = el => el.querySelector('a[href*="/jobs/view/"]')?.href?.match(/(\d+)/)?.[1] || 
                            el.innerText?.split('\n').slice(0,2).join('|');

        const scrollAndLoad = async () => {
            const oldHeight = cont.scrollHeight;
            cont.scrollTo({ top: cont.scrollHeight, behavior: 'smooth' });
            await new Promise(r => setTimeout(r, 1500));
            return cont.scrollHeight > oldHeight;
        };

        for (let idle = 0; idle < 4;) {
            let clicked = 0;
            
            for (const el of getCards()) {
                const id = getId(el);
                if (!id || seen.has(id)) continue;
                seen.add(id);

                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                await new Promise(r => setTimeout(r, 600 + Math.random() * 600));
                
                // Click job
                el.click();
                                   
                let tries = 0;
                while (tries < 10) {
                    await new Promise(r => setTimeout(r, 300));
                    if (document.querySelector('.jobs-description__content')) break;
                    tries++;
                }
                                   
                // Extract job details
                const title = el.innerText?.split('\n')[0] || null;
                const company = document.getElementsByClassName('job-details-jobs-unified-top-card__company-name')[0]?.textContent?.trim() || null;
                const description = document.querySelector('.jobs-description__content')?.innerText || null;

                await new Promise(r => setTimeout(r, 1000 + Math.random() * 500));
                const url = `https://www.linkedin.com/jobs/view/${id}/`;

                results.push({id, url, title, company, description});
                clicked++;
            }
            
            const newContent = await scrollAndLoad();
            idle = clicked ? 0 : idle + 1;
        }
        
        return results;
    };

    const allResults = [];
    let pageNumber = 1;
    
    while (true) {
        console.log(`🔄 Processing page ${pageNumber}...`);
        
        // Process current page
        const pageResults = await processCurrentPage();
        allResults.push(...pageResults);
        
        console.log(`✅ Page ${pageNumber} done: ${pageResults.length} jobs found (Total: ${allResults.length})`);
        
        // Look for next button
        const nextButton = document.querySelector('button[aria-label="View next page"], .jobs-search-pagination__button--next');
        
        if (!nextButton || nextButton.disabled) {
            console.log(`🏁 No more pages. Final count: ${allResults.length} jobs`);
            break;
        }
        
        // Click next button and wait for page to load
        console.log(`➡️ Going to next page...`);
        nextButton.click();
        
        // Wait for new page to load
        await new Promise(r => setTimeout(r, 3000 + Math.random() * 2000));
        
        // Wait for content to be ready
        let loadTries = 0;
        while (loadTries < 10) {
            const cont = document.getElementsByClassName('scaffold-layout__list')[0]?.children?.[1];
            if (cont && cont.getElementsByClassName('job-card-container--clickable').length > 0) {
                break;
            }
            await new Promise(r => setTimeout(r, 500));
            loadTries++;
        }
        
        pageNumber++;
        
        // Safety check to prevent infinite loops
        if (pageNumber > 50) {
            console.log(`⚠️ Reached page limit (50), stopping...`);
            break;
        }
    }
    
    console.log(`🎉 All done! Processed ${pageNumber - 1} pages, found ${allResults.length} total jobs`);
    return JSON.stringify(allResults, null, 2);
    })();
""")
        
        jobs = json.loads(jobs)
        df = pd.DataFrame(jobs)
        df.to_json("linkedin_jobs.json", indent=2, force_ascii=False)



       

        # # Click each job
        # await click_jobs(job_containers, page)

        print(f"✅ Opened {site_url} with profile: {profile_name}")

        while ctx.pages:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

