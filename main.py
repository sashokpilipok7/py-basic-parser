import asyncio
import logging
import os
from typing import Callable

from aiohttp import web
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from scraper import get_work_ua_jobs

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN') or ""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Web Server Part for Render ---
async def health_check(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Get port from environment or default to 8080
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Web server started on port {port}")

# --- Bot Part ---

async def cmd_base_jobs(message: types.Message, base_func: Callable):
    print(message.quote)
    await message.answer("Шукаю вакансії, зачекайте...")
    # jobs = await get_work_ua_jobs()
    jobs = []
    if not jobs:
        await message.answer("Не вдалося знайти вакансії або сталася помилка.")
        return

    # Send first 5 jobs to avoid flooding
    for job in jobs[:5]:
        response_text = f"<b>{job['title']}</b>\n{job['link']}"
        await message.answer(response_text, parse_mode="HTML")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт! \n Напишіть /jobs_dou щоб отримати свіжі вакансії розробника. \n Або /jobs_lawyer щоб отримати свіжі юридичні вакансії.")

@dp.message(Command("jobs_dou"))
async def cmd_jobs_dou(message: types.Message):
    return await cmd_base_jobs(message, get_work_ua_jobs)

@dp.message(Command("jobs_lawyer"))
async def cmd_jobs_lawyer(message: types.Message):
    return await cmd_base_jobs(message, get_work_ua_jobs)

async def main():
    # Start the web server concurrently with the bot polling
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
