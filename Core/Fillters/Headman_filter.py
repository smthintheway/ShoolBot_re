from aiogram import Bot
import json
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from Services.UserService import UserService

with open('Core/settings.json') as f:
    config = json.load(f)

class IsHeadman(BaseFilter):

    async def __call__(self, msg: Message|CallbackQuery, bot: Bot, user_service: UserService):
        user_data = await user_service.get_user_info(tg_id=msg.from_user.id)
        user_data = user_data['privileges']
        if user_data in (config['Privileges'][0],config['Privileges'][1],config['Privileges'][2]):
            print('admin')
            return True
        else:
            return False

