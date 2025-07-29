import uuid, hashlib
from pathlib import Path
from aiogram import types,Router,F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import  AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from Presentation.Templates.Subjects import subject_task_presentation
from Core.State_Fillters.Subjects import Subject_actions
from Core.Fillters.Headman_filter import IsHeadman
from Services.SubjectService import SubjectService
from Services.UserDataService import UserService
from Presentation.Keyboards.Mini_keyboards import Edit_ask_keyboard, Types_keyboard, Binary_keyboard,Menu_button_keyboard

database_engine = create_async_engine('sqlite+aiosqlite:///main.db')
async_session = sessionmaker(database_engine,class_=AsyncSession,expire_on_commit=False)


Hometasks_Router = Router()

async def save_media(msg: types.Message, media_dir: Path,existing_content: str ='') -> tuple[str, Path]:
    if msg.photo: file = msg.photo[-1]
    elif msg.document: file = msg.document

    file_info = await msg.bot.get_file(file.file_id)
    file_ext = file_info.file_path.split('.')[-1].lower() if '.' in file_info.file_path else 'bin'

    salt = uuid.uuid4().hex[:8]
    hash_name = hashlib.sha256(f"{file.file_unique_id}{salt}".encode()).hexdigest()[:16]
    safe_filename = f'{hash_name}.{file_ext}'

    file_path = media_dir / safe_filename

    await msg.bot.download(file.file_id, file_path)

    relative_path = f"Users_media/{safe_filename}"
    updated_content = f'{existing_content} {relative_path}' if existing_content else relative_path

    return updated_content, file_path


@Hometasks_Router.callback_query(F.data == 'Hometask_switch')
async def hometask_switch(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.edit_text(text='Что бы вы хотели сделать?',reply_markup=Edit_ask_keyboard)
    await state.set_state(Subject_actions.switch_choose)

@Hometasks_Router.callback_query(F.data == 'edit', Subject_actions.switch_choose,IsHeadman())
async def hometask_edit_start(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.answer(text = 'Введите название предмета\n(Для предметов по типу Русского языка используйте одно слово. Например Русский)')
    await state.set_state(Subject_actions.edit_SubjectName)

@Hometasks_Router.message(F.text, Subject_actions.edit_SubjectName,IsHeadman())
async def hometask_edit_name(msg: types.Message, state: FSMContext):
    await state.update_data(subject_name = msg.text)
    await msg.answer(text = 'Введите для какой группы будет доступно дз\n(Если групп нет напишите 0)')
    await state.set_state(Subject_actions.edit_SubjectGroup)

@Hometasks_Router.message(F.text, Subject_actions.edit_SubjectGroup,IsHeadman())
async def hometask_edit_group(msg: types.Message, state: FSMContext):
    try:
        await state.update_data(group = int(msg.text))
        await msg.answer(text='Какого типа будет дз?',reply_markup=Types_keyboard)
        await state.set_state(Subject_actions.switch_type)
    except Exception:
        await msg.answer(text = 'Возможно вы ввели не число. Попробуйте снова')


@Hometasks_Router.callback_query(F.data == 'text', Subject_actions.switch_type,IsHeadman())
async def hometask_edit_text(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type = 'text')
    await callback.message.edit_text(text = 'Введите новое дз')
    await state.set_state(Subject_actions.edit_SubjectContent)


@Hometasks_Router.callback_query(F.data.in_(['photo','data']), Subject_actions.switch_type,IsHeadman())
async def hometask_edit_media(callback: types.CallbackQuery, state: FSMContext):
    match F.data:
        case 'photo': await state.update_data(type = 'photo')
        case 'document': await state.update_data(type = 'document')

    await callback.message.answer(text = 'Введите количество медиа-файлов в виде числа')
    await state.set_state(Subject_actions.edit_SubjectContent_Count)

@Hometasks_Router.message(F.text, Subject_actions.edit_SubjectContent_Count,IsHeadman())
async def set_iterations_count(msg: types.Message, state: FSMContext):
    try:
        count = int(msg.text)
        await state.update_data(media_content_count = count)
        await msg.answer(text = 'Присылайте медиа-контент по одному файлу')
        await state.update_data(content = '')
        await state.set_state(Subject_actions.edit_SubjectContent)
    except TypeError:
        await msg.answer(text = 'Возможно вы ввели не число. Попробуйте снова')

@Hometasks_Router.message(F.photo or F.document, Subject_actions.edit_SubjectContent,IsHeadman())
async def subject_edit_media(msg: types.Message,state: FSMContext):
     data = await state.get_data()
     rest_count = int(data.get('media_content_count'))
     project_root = Path(__file__).resolve().parent.parent.parent
     media_dir = project_root / 'Users_media'

     if rest_count <= 1:
        await msg.answer(text = 'Хотите добавить коментарий?', reply_markup=Binary_keyboard)
        await state.set_state(Subject_actions.switch_comments)

     if msg.photo or msg.document:
         new_content, _ = await save_media(msg,media_dir,data.get('content', ''))

         await state.update_data(content = new_content,
                                 media_content_count = rest_count -1)

         if rest_count >= 1:
            await msg.answer(text=f'Файл сохранен. Файлов осталось: {rest_count-1}')

     if rest_count == 0:
         await msg.answer(text='Хотите добавить коментарий?', reply_markup=Binary_keyboard)
         await state.set_state(Subject_actions.switch_comments)




@Hometasks_Router.message(F.text, Subject_actions.edit_SubjectContent,IsHeadman())
async def subject_edit_text(msg: types.Message, state: FSMContext):
    await state.update_data(content = msg.text)
    await msg.answer(text = 'Хотите добавить коментарий?', reply_markup=Binary_keyboard)
    await state.set_state(Subject_actions.switch_comments)

@Hometasks_Router.callback_query(F.data == 'yes', Subject_actions.switch_comments, IsHeadman())
async def hometask_edit_comment(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите новый коментарий')
    await state.set_state(Subject_actions.edit_SubjectComment)

@Hometasks_Router.callback_query(F.data == 'no', Subject_actions.switch_comments,IsHeadman())
async def hometask_edit_over(callback: types.CallbackQuery, state: FSMContext, user_service: UserService, subject_service: SubjectService):
        data = await state.get_data()
        await callback.message.edit_text(text='Изменение завершено', reply_markup=Menu_button_keyboard)

        user_data = await user_service.get_user_info(tg_id=callback.from_user.id)
        result = await subject_service.add_task(subject_name=data.get('subject_name'),
                                             form=user_data['form'],
                                             editor=user_data['username'],
                                             comment=None,
                                             hw_type=data.get('type'),
                                             content=data.get('content'))

        await state.update_data({})
        await state.clear()

@Hometasks_Router.message(F.text, Subject_actions.edit_SubjectComment,IsHeadman())
async def subject_edit_comment(msg: types.Message, state: FSMContext, user_service: UserService, subject_service: SubjectService):
    await state.update_data(comment=msg.text)
    data = await state.get_data()
    await msg.answer(text='Изменение завершено', reply_markup=Menu_button_keyboard)
    user_data = await user_service.get_user_info(tg_id=msg.from_user.id)
    result = await subject_service.add_task(subject_name=data.get('subject_name'),
                                            form=user_data['form'],
                                            editor=user_data['username'],
                                            comment=data.get('comment'),
                                            hw_type=data.get('type'),
                                            content=data.get('content'))


    await state.update_data({})
    await state.clear()

@Hometasks_Router.callback_query(F.data == 'ask',Subject_actions.switch_choose)
async def ask_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введи название интересующего предмета',reply_markup=Menu_button_keyboard)
    await state.set_state(Subject_actions.ask_SubjectName)

@Hometasks_Router.message(F.text, Subject_actions.ask_SubjectName)
async def ask_one_task(msg: types.Message,state: FSMContext, user_service: UserService, subject_service: SubjectService):
    user_data = await user_service.get_user_info(tg_id=msg.from_user.id)
    subject = await subject_service.get_subject_note(subject_name=msg.text,form=user_data['form'],group=user_data['group'])
    print(subject)
    await subject_task_presentation(subject,msg)