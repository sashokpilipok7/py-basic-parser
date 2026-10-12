import asyncio
from scraper import get_work_ua_jobs

async def test_scraper():
    jobs = await get_work_ua_jobs()
    if jobs:
        print(f"Successfully fetched {len(jobs)} jobs.")
        print(repr(jobs[0]['title']))
    else:
        print("Failed to fetch jobs.")

if __name__ == "__main__":
    asyncio.run(test_scraper())
