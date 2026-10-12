import os
import asyncio
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from scraper import get_work_ua_jobs

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Напишіть /jobs щоб отримати актуальні вакансії.")

@dp.message(Command("jobs"))
async def cmd_jobs(message: types.Message):
    await message.answer("Шукаю вакансії, зачекайте...")
    jobs = await get_work_ua_jobs()
    
    if not jobs:
        await message.answer("Не вдалося знайти вакансії або сталася помилка.")
        return
    
    # Send first 5 jobs to avoid flooding
    for job in jobs[:5]:
        response_text = f"<b>{job['title']}</b>\n{job['link']}"
        await message.answer(response_text, parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
