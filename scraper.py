import asyncio
import concurrent.futures
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

URL = "https://www.work.ua/jobs-remote-розробник/?employment=75&sort=date"

async def get_work_ua_jobs():
    def fetch_url():
        req = Request(
            url=URL,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urlopen(req) as response:
            return response.read()

    loop = asyncio.get_running_loop()
    try:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            html_content = await loop.run_in_executor(pool, fetch_url)
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []
    
    # Try decoding with utf-8 or windows-1251
    try:
        html_decoded = html_content.decode('utf-8')
    except UnicodeDecodeError:
        html_decoded = html_content.decode('windows-1251')
    
    soup = BeautifulSoup(html_decoded, "html.parser")
    
    jobs = []
    for h2 in soup.find_all("h2", class_="my-0"):
        a_tag = h2.find("a")
        if a_tag and a_tag.get("href"):
            title = a_tag.text.strip()
            link = "https://www.work.ua" + a_tag.get("href")
            jobs.append({"title": title, "link": link})
            
    return jobs
