import html


def format_jobs_message(jobs: list[dict]) -> str:
    """Format a list of job dicts into an HTML string for Telegram."""
    return "\n\n".join(
        f"<b>{html.escape(job['title'])}</b>\n{job['link']}" for job in jobs
    )
