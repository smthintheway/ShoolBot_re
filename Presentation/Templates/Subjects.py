from aiogram.utils.media_group import MediaGroupBuilder
from Infrastructure.Database.Tables.Subjects import Subjects
from aiogram.types import FSInputFile, Message


async def subject_task_presentation(subject: Subjects,msg: Message):
    subject = subject[0]
    if subject.type == 'photo' or subject.type == 'document':
        media = subject.homework.split()
        if subject.comment:
            answer_text = f'{subject.comment}\n{subject.date}'
        else:
            answer_text = f'{subject.date}'
        builder = MediaGroupBuilder(caption=answer_text)
        async for i in media:
            builder.add(type=subject.type,media=FSInputFile(f"{i}"))
        await msg.answer_media_group(media=builder.build())

    elif subject.type == 'text':
        if subject.comment:
            await  msg.answer(text=f'{subject.subject_name}\nДомашнее задание: {subject.homework}\nКоментарии к заданию {subject.comment}\n{subject.date}')