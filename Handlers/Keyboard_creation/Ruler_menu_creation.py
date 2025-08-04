from Presentation.Keyboards.Rulers_menus import *
from aiogram import types,Router,F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from Presentation.Templates.Subjects import subject_task_presentation
from Core.State_Fillters.Privilege_State import Privilege_update
from Core.Fillters.Headman_filter import IsHeadman, IsHealper
from Core.Fillters.Admin_filter import IsAdmin, IsSupAdmin
from Services.UserDataService import UserService

RulerMenu_Router = Router()

@RulerMenu_Router.callback_query(F.data == 'Admin_switch',IsSupAdmin)
async def supadmin_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Меню глав. администратора',reply_markup=supadmin_menu)

@RulerMenu_Router.callback_query(F.data == 'Admin_switch',IsAdmin)
async def supadmin_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Меню администратора',reply_markup=admin_menu)

@RulerMenu_Router.callback_query(F.data == 'Admin_switch',IsHeadman)
async def supadmin_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Меню старосты',reply_markup=headman_menu)

@RulerMenu_Router.callback_query(F.data == 'Admin_switch',IsHealper)
async def supadmin_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(text='К сожалению вам не разрешенно пользоваться данным меню')

