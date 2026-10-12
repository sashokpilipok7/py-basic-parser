import httpx
from bs4 import BeautifulSoup

# Use a realistic User-Agent to avoid 403
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

URL = "https://www.work.ua/jobs-km-lawyer/?sort=date"


def get_work_ua_jobs(client: httpx.Client, url: str = URL):
    response = client.get(url, headers=HEADERS)
    print(f"Status Code: {response.status_code}")

    if response.status_code != 200:
        print("Failed to fetch page")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    jobs = []
    # Find all h2 with class 'my-0'
    for h2 in soup.find_all("h2", class_="my-0"):
        a_tag = h2.find("a")
        if a_tag and a_tag.get("href"):
            title = a_tag.text.strip()
            # The href might be a relative path
            link = "https://www.work.ua" + a_tag.get("href")
            jobs.append({"title": title, "link": link})

    return jobs


def main_parser():
    with httpx.Client() as client:
        jobs = get_work_ua_jobs(client, URL)
        for job in jobs:
            print(f"Title: {job['title']}")
            print(f"Link: {job['link']}")
            print("-" * 20)


if __name__ == '__main__':
    main_parser()