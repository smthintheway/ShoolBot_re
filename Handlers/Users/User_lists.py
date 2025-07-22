import json
from aiogram.filters.command import Command
from aiogram import types,Router,F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_session, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from Core.State_Fillters.User_State import User_fsm
from Presentation.Templates.Registration import *
from Services.UsersListsService import ListService,ListRepository
from Services.UserService import UserService, UserRepository
from Presentation.Keyboards.Mini_keyboards import Menu_button_keyboard
from Presentation.Keyboards.Main_menu import main_menu

List_Router = Router()

database_engine = create_async_engine('sqlite+aiosqlite:///main.db')
async_session = sessionmaker(database_engine,class_=AsyncSession,expire_on_commit=False)

@List_Router.message(Command('list'))
async def show_admins(msg: types.Message,state: FSMContext):
    async with async_session() as session:
        us_repo = UserRepository(session)
        user_service = UserService(us_repo)
        list_repo = ListRepository(session)
        list_service = ListService(list_repo)

        user_form = await user_service.get_user_info(tg_id=msg.from_user.id)
        user_form = user_form['form']

        test_list= await list_service.get_privilege_list(privilege='admin',form=user_form)
        print(test_list)