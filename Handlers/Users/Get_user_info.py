from Presentation.Templates.Registration import user_info_template
from Services.UserService import UserService,UserRepository
from Presentation.Keyboards.Mini_keyboards import Menu_button_keyboard
from Presentation.Keyboards.Main_menu import main_menu
from sqlalchemy.ext.asyncio import async_session, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from aiogram import types,Router,F

database_engine = create_async_engine('sqlite+aiosqlite:///main.db')
async_session = sessionmaker(database_engine,class_= AsyncSession,expire_on_commit=False)

Get_user_info_Router = Router()

@Get_user_info_Router.callback_query(F.data == 'Show_user_data')
async def show_user_data(callback: types.CallbackQuery):
    try:
        async with async_session() as session:
            us_repo = UserRepository(session)
            user_service = UserService(us_repo)

        user_data = await user_service.get_user_info(tg_id=callback.from_user.id)
        await callback.message.edit_text(text=user_info_template(
            username = user_data['username'],
            tg_id = user_data['tg_id'],
            form=user_data['form'],
            group=user_data['group'],
            privileges=user_data['privileges']),
            reply_markup=Menu_button_keyboard)

    except Exception as error:
        print(error)