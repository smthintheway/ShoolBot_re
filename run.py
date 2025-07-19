import asyncio
import logging
import json
from Core.di import setup_di
from aiogram import Bot, Dispatcher
from Handlers.Users.Registration import Registration_Router
from Handlers.Users.Update_user_data import User_data_update_Router
from Handlers.Users.Get_user_info import Get_user_info_Router

logging.basicConfig(level=logging.INFO)

async def main():
    with open('Core/settings.json') as f:
        settings = json.load(f)
    Token = settings['Token']
    bot = Bot(Token)
    ds = Dispatcher()
    setup_di(ds)
    ds.include_router(Registration_Router)
    ds.include_router(Get_user_info_Router)
    ds.include_router(User_data_update_Router)
    await ds.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())