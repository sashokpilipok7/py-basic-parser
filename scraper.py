import logging
from bs4 import BeautifulSoup
from utils.http import fetch_html

SOURCES = {
    "jobs_dou": ("https://jobs.dou.ua/vacancies/?search=Fullstack&exp=1-3", lambda s: parse_from_dou(s)),
    "jobs_lawyer": ("https://www.work.ua/jobs-remote-%D1%8E%D1%80%D0%B8%D1%81%D1%82/", lambda s: parse_from_work_ua(s)),
}


def parse_from_work_ua(soup: BeautifulSoup) -> list:
    jobs = []
    for h2 in soup.find_all("h2", class_="my-0"):
        a_tag = h2.find("a")
        if a_tag and a_tag.get("href"):
            jobs.append({
                "title": a_tag.text.strip(),
                "link": f"https://www.work.ua{a_tag.get('href')}"
            })
    return jobs


def parse_from_dou(soup: BeautifulSoup) -> list:
    jobs = []
    for li in soup.find_all("li", class_="l-vacancy"):
        a_tag = li.find("a", class_="vt")
        if a_tag and a_tag.get("href"):
            jobs.append({
                "title": a_tag.text.strip(),
                "link": a_tag.get("href")
            })
    return jobs


async def get_work_ua_jobs(query: str = "jobs_dou") -> list:
    key = query.lstrip("/")
    source = SOURCES.get(key)
    if not source:
        return []

    url, parser = source
    try:
        html = await fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")
        return parser(soup)
    except Exception as e:
        logging.error(f"Error fetching jobs for {query}: {e}")
        return []


get_jobs = get_work_ua_jobs
