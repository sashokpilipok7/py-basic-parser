import time
import httpx
from bs4 import BeautifulSoup

URL = "https://www.work.ua/jobs-km-lawyer/?sort=date"
# URL = "https://www.cathedralkp.org.ua/events"

def get_work_ua_jobs(page: int, client: httpx.Client, url: str = URL):
    # response = client.get(url, params={"page": page})
    response = client.get(url)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")

    return [
       job.text.strip() for job in soup.find_all("h3")
    ]

def main_parser(start_page, end_page):
    with httpx.Client() as client:
        for page in range(start_page, end_page):
            print(get_work_ua_jobs(page, client, URL))

if __name__ == '__main__':
    main_parser(start_page=0, end_page=1)