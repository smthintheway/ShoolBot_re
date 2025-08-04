import asyncio
import logging
import json
from Core.di import Container, DIMiddleware
from aiogram import Bot, Dispatcher
from Handlers.Users.Registration import Registration_Router
from Handlers.Users.Update_user_data import User_data_update_Router
from Handlers.Users.User_lists import List_Router
from Handlers.Users.Get_user_info import Get_user_info_Router
from Handlers.Subjects.Schedule import Schedule_Router
from Handlers.Subjects.Hometasks import Hometasks_Router
from Handlers.Keyboard_creation.Ruler_menu_creation import RulerMenu_Router

logging.basicConfig(level=logging.INFO)

async def main():
    with open('Core/settings.json') as f:
        settings = json.load(f)
    container = Container()
    di_middleware = DIMiddleware(container)
    Token = settings['Token']
    bot = Bot(Token)
    ds = Dispatcher()
    ds.update.middleware.register(di_middleware)
    ds['container'] = container
    ds.include_router(Registration_Router)
    ds.include_router(Get_user_info_Router)
    ds.include_router(User_data_update_Router)
    ds.include_router(List_Router)
    ds.include_router(Hometasks_Router)
    ds.include_router(Schedule_Router)
    ds.include_router(RulerMenu_Router)
    await ds.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())