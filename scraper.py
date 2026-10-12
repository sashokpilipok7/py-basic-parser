import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.work.ua/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1"
}

URL = "https://www.work.ua/jobs-remote-розробник/?employment=75&sort=date"

async def get_work_ua_jobs():
    async with httpx.AsyncClient() as client:
        response = await client.get(URL, headers=HEADERS)
        print(f"DEBUG: Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code != 200:
            return []

        # Try decoding with windows-1251 if utf-8 fails or is incorrect
        try:
            html_content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            html_content = response.content.decode('windows-1251')
        
        soup = BeautifulSoup(html_content, "html.parser")
        
        jobs = []
        for h2 in soup.find_all("h2", class_="my-0"):
            a_tag = h2.find("a")
            if a_tag and a_tag.get("href"):
                title = a_tag.text.strip()
                link = "https://www.work.ua" + a_tag.get("href")
                jobs.append({"title": title, "link": link})
                
        return jobs
