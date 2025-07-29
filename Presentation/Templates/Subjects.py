from aiogram.utils.media_group import MediaGroupBuilder
from Infrastructure.Database.Tables.Subjects import Subjects
from aiogram.types import FSInputFile, Message
from Presentation.Keyboards.Mini_keyboards import Menu_button_keyboard


async def subject_task_presentation(subject: Subjects,msg: Message):
    if subject is not None:
        if subject.type == 'photo' or subject.type == 'document':
            media = subject.homework.split()
            if subject.comment is not None:
                answer_text = f'{subject.comment}\nОтправлено @{subject.editor} в {subject.date}'
            else:
                answer_text = f'Отправлено @{subject.editor} в {subject.date}'
            builder = MediaGroupBuilder(caption=answer_text)
            for i in media:
                builder.add(type=subject.type,media=FSInputFile(f"{i}"))
            await msg.answer_media_group(media=builder.build(),reply_markup=Menu_button_keyboard)

        elif subject.type == 'text':
            if subject.comment is not None:
                await  msg.answer(text=f'{subject.subject_name}\nДомашнее задание: {subject.homework}\nКоментарии к заданию: {subject.comment}\nОтправлено @{subject.editor} в {subject.date}',
                                  reply_markup=Menu_button_keyboard)
            else:
                await msg.answer(
                    text=f'{subject.subject_name}\nДомашнее задание: {subject.homework}\nОтправлено @{subject.editor} в {subject.date}',
                    reply_markup=Menu_button_keyboard)
    else:
        await msg.answer(text='Записи об этом предмете не найдено',reply_markup=Menu_button_keyboard)