from aiogram import types,Router,F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import  AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from Presentation.Templates.Subjects import subject_task_presentation
from Core.State_Fillters.Privilege_State import Privilege_update
from Core.Fillters.Headman_filter import IsHeadman
from Services.PrivilegeService import PrivilegeService
from Services.UserDataService import UserService
from Presentation.Keyboards.Mini_keyboards import Edit_ask_keyboard, Types_keyboard, Binary_keyboard,Menu_button_keyboard

Privilege_Router = Router()

@Privilege_Router.message(Command('add new admin'))
async def add_new_admin(msg: types.Message, privilege_service: PrivilegeService, state: FSMContext):
    await msg.edit_text(text='Введите id или имя пользователя')
    await state.set_state(Privilege_update.choosing_person)
    
