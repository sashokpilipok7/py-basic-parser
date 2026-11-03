import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from dotenv import load_dotenv

from scraper import get_work_ua_jobs
from utils.formatters import format_jobs_message
from utils.server import start_web_server

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") or ""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# In-memory storage for pagination: {user_id: {"jobs": [...], "offset": int}}
user_jobs_cache: dict[int, dict] = {}


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт!\n"
        "Напишіть /jobs_dou щоб отримати свіжі вакансії розробника.\n"
        "Або /jobs_lawyer щоб отримати свіжі юридичні вакансії."
    )


@dp.message(Command("jobs_dou", "jobs_lawyer"))
async def cmd_jobs(message: types.Message, command: CommandObject):
    await message.answer("Шукаю вакансії, зачекайте...")
    jobs = await get_work_ua_jobs(command.command)
    if not jobs:
        await message.answer("Не вдалося знайти вакансії або сталася помилка.")
        return

    # Send first 5 jobs
    first_batch = jobs[:5]
    await message.answer(format_jobs_message(first_batch), parse_mode="HTML")

    # If more jobs exist, cache them and send load more hint
    if len(jobs) > 5 and message.from_user:
        user_jobs_cache[message.from_user.id] = {
            "jobs": jobs,
            "offset": 5
        }
        await message.answer(
            "Знайдено більше вакансій! Надішліть /more_jobs (або /more-jobs), щоб завантажити наступні 5."
        )


@dp.message(Command("more_jobs", "more-jobs"))
async def cmd_more_jobs(message: types.Message):
    user_id = message.from_user.id if message.from_user else None
    state = user_jobs_cache.get(user_id) if user_id else None

    if not state or state["offset"] >= len(state["jobs"]):
        await message.answer(
            "Немає збережених вакансій для завантаження.\n"
            "Спочатку оберіть категорію: /jobs_dou або /jobs_lawyer"
        )
        return

    jobs = state["jobs"]
    offset = state["offset"]
    batch = jobs[offset : offset + 5]
    state["offset"] += len(batch)

    await message.answer(format_jobs_message(batch), parse_mode="HTML")

    if state["offset"] < len(jobs):
        remaining = len(jobs) - state["offset"]
        await message.answer(
            f"Залишилось ще {remaining} вакансій. Надішліть /more_jobs щоб завантажити більше."
        )
    else:
        user_jobs_cache.pop(user_id, None)
        await message.answer("Це всі доступні вакансії за цим запитом.")


async def main():
    await start_web_server()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
