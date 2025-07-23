from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

menu_buttons = [[InlineKeyboardButton(callback_data='Hometask_switch',text='Домашнее задание'),
         InlineKeyboardButton(callback_data='Table_switch',text='Расписание')],
        [InlineKeyboardButton(callback_data='Show_classmates',text='Мои одноклассники')],
        [InlineKeyboardButton(callback_data='Show_user_data',text='Мои данные')],
        [InlineKeyboardButton(callback_data='Change_user_data',text='Изменить данные о себе')],
        [InlineKeyboardButton(callback_data='Admin_switch',text='Панель администратора')]]

main_menu = InlineKeyboardMarkup(inline_keyboard=menu_buttons)

