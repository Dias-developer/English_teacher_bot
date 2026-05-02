from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from os import getenv
import asyncio
from commands import router
import logging

load_dotenv()
TOKEN = getenv("TOKEN")
dp = Dispatcher()

dp.include_router(router)

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    print('Start...')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot off")
