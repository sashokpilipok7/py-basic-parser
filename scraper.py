import asyncio
import concurrent.futures
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

URL = "https://jobs.dou.ua/vacancies/?search=Fullstack&exp=1-3"

def parse_from_work_ua(soup: BeautifulSoup) -> list:
    jobs = []
    for h2 in soup.find_all("h2", class_="my-0"):
        a_tag = h2.find("a")
        if a_tag and a_tag.get("href"):
            title = a_tag.text.strip()
            link = "https://www.work.ua" + a_tag.get("href")
            jobs.append({"title": title, "link": link})
    return jobs

def parse_from_dou(soup: BeautifulSoup) -> list:
    jobs = []
    for h2 in soup.find_all("li", class_="l-vacancy"):
        a_tag = h2.find("a", class_="vt")
        if a_tag and a_tag.get("href"):
            title = a_tag.text.strip()
            link = a_tag.get("href")
            jobs.append({"title": title, "link": link})
    return jobs

async def get_work_ua_jobs():
    def fetch_url():
        req = Request(
            url=URL,
            headers={'User-Agent': 'Mozilla/5.0',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                     'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
                     'Rate-limit': '3',
                     'Connection': 'keep-alive',
                     "Upgrade-Insecure-Requests": "1",
                     "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                     "Sec-Ch-Ua-Mobile": "?0",
                     "Sec-Ch-Ua-Platform": '"Windows"',
                     "Sec-Fetch-Dest": "document",
                     "Sec-Fetch-Mode": "navigate",
                     "Sec-Fetch-Site": "none",
                     "Sec-Fetch-User": "?1"
                     }
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
    
    return parse_from_dou(soup)
