import json
from aiogram import types,Router,F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_session, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from Core.State_Fillters.User_State import User_fsm
from Presentation.Templates.Registration import *
from Services.UserDataService import UserService,UserRepository
from Presentation.Keyboards.Mini_keyboards import Menu_button_keyboard
from Presentation.Keyboards.Main_menu import main_menu


database_engine = create_async_engine('sqlite+aiosqlite:///main.db')
async_session = sessionmaker(database_engine,class_=AsyncSession,expire_on_commit=False)

User_data_update_Router = Router()


@User_data_update_Router.callback_query(F.data == 'Change_user_data')
async def start_handler(callback: types.CallbackQuery,state: FSMContext):
    try:
        async with async_session() as session:
            us_repo = UserRepository(session)
            user_service = UserService(us_repo)

            check = await user_service.get_user_reg(callback.from_user.id)
            if not(check is None):
                await callback.message.answer(text=user_edit_form)
                await state.set_state(User_fsm.updating_form)
    except Exception as error:
        print(error)


@User_data_update_Router.message(F.text,User_fsm.updating_form)
async def edit_user_form(msg: types.Message,state: FSMContext):
    try:
        with open('Core/settings.json') as f:
            config = json.load(f)

        Forms = config['Forms']
        if msg.text in Forms:
            await state.update_data(form = msg.text)
            await state.set_state(User_fsm.updating_group)
            await msg.answer(text=user_edit_group)
        else:
            await msg.answer('Такого класса нет в списках\nЕсли произошла ошибка обратитесь к администратору')
            await msg.answer(text='Повторите попытку')
    except Exception as error:
        print(error)


@User_data_update_Router.message(F.text, User_fsm.updating_group)
async def edit_user_group(msg: types.Message, state: FSMContext, user_service: UserService):
    try:
            await state.update_data(group = msg.text)
            data = await state.get_data()
            await msg.answer(text=user_info_template(
                    username=msg.from_user.username,
                    form=data.get('form'),
                    group=data.get('group'),
                    privileges='Ученик',
                    tg_id=msg.from_user.id),
                    reply_markup=Menu_button_keyboard)

            await user_service.registration({'tg_id': msg.from_user.id,
                                                 'username': msg.from_user.username,
                                                 'form': data.get('form'),
                                                 'group': data.get('group'),
                                                 'privileges': 'Ученик'
                                                 })

            await state.set_data({})
            await state.set_state(User_fsm.update_over)
    except Exception as error:
        print(error)

@User_data_update_Router.callback_query(F.data == 'back_to_menu')
async def menu_switch(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(text='Меню',reply_markup = main_menu)
        await state.clear()
    except Exception as error:
        print(error)