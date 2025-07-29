import json
from aiogram.filters.command import Command
from aiogram import types,Router,F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_session, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Services.UsersListsService import ListService,ListRepository
from Services.UserDataService import UserService, UserRepository

List_Router = Router()

database_engine = create_async_engine('sqlite+aiosqlite:///main.db')
async_session = sessionmaker(database_engine,class_=AsyncSession,expire_on_commit=False)

async def build_page(msg: types.Message | types.CallbackQuery, state: FSMContext, page: int = 0):
    with open('Core/settings.json') as f:
        config = json.load(f)
        person_per_page = config['Users_per_page']

    data = await state.get_data()
    users = data.get('users_list')
    start_index = page*person_per_page
    end_index = start_index+person_per_page
    users_to_show = users[start_index:end_index]
    page_count = (len(users)+person_per_page-1)//person_per_page
    text = ''
    for i in users_to_show:
        text = text+f'@{i.username}\nКласс: {i.form}\nГруппа: {i.group}\nСтатус: {i.privileges}\n'

    text = text+f'Страница {page+1}/{page_count}'

    button_builder = InlineKeyboardBuilder()
    if page>0:
        button_builder.button(text='Назад',callback_data=f'prev_{page}')
    if end_index < len(users):
        button_builder.button(text = 'Вперед', callback_data=f'next_{page}')
    button_builder.button(text='В меню', callback_data='back_to_menu')
    button_builder.adjust(2)

    if isinstance(msg, types.Message):
        await msg.answer(text=text,reply_markup=button_builder.as_markup())
    elif isinstance(msg, types.CallbackQuery):
        await msg.message.edit_text(text = text, reply_markup = button_builder.as_markup())


@List_Router.callback_query(F.data.startwith('prev_') or F.data.startwith('next_'))
async def pagination(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split('_')[0]
    current_page = int(callback.data.split('_')[1])
    new_page = current_page
    match action:
        case 'prev':
            new_page = current_page - 1
        case 'next':
            new_page = current_page + 1

    await build_page(msg=callback,page=new_page,state= state)




@List_Router.callback_query(F.data == 'Show_classmates')
async def show_admins(callback: types.CallbackQuery,state: FSMContext, user_service: UserService, list_service: ListService):
        user_form = await user_service.get_user_info(tg_id=callback.from_user.id)
        user_form = user_form['form']
        classmates = await list_service.get_classmates_list(form=user_form)
        await state.update_data(users_list = classmates)
        await build_page(callback, state)

@List_Router.message(Command('admin_list'))
async def show_admins(msg: types.Message, state: FSMContext):
    async with async_session() as session:
        list_repo = ListRepository(session)
        list_service = ListService(list_repo)

        with open('Core/settings.json') as f:
            config = json.load(f)

        admins = await list_service.get_privilege_list(form = None,privilege=config['Privileges'][1])
        await state.update_data(users_list = admins)
        await build_page(msg, state)

@List_Router.message(Command('headman_list'))
async def show_headmen(msg: types.Message, state: FSMContext, user_service: UserService, list_service: ListService):
    async with async_session() as session:


        with open('Core/settings.json') as f:
            config = json.load(f)

        user_form = await user_service.get_user_info(tg_id=msg.from_user.id)
        user_form = user_form['form']
        headmen = await list_service.get_privilege_list(form = user_form, privilege = config['Privileges'][2])
        await state.update_data(users_list = headmen)
        await build_page(msg, state)