from aiogram.types import (InlineKeyboardButton,InlineKeyboardMarkup)


admin_buttons = [[InlineKeyboardButton(callback_data='admin_list',text='Список администраторов')],
                      [InlineKeyboardButton(callback_data='headman_list',text='Список старост')],
                      [InlineKeyboardButton(callback_data='manual_add_admin',text='Добавить старосту')],
                      [InlineKeyboardButton(callback_data='manual_delete_admin',text='Удалить старосту')],
                      [InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]

admin_menu = InlineKeyboardMarkup(inline_keyboard=admin_buttons)

headman_buttons = [[InlineKeyboardButton(callback_data='responsible_list',text='Список ответственных'),],
                 [InlineKeyboardButton(callback_data='classmates_list',text='Список одноклассников')],
                 [InlineKeyboardButton(callback_data='add_new_resposible',text='Добавить ответственого')],
                 [InlineKeyboardButton(callback_data='delete_resposible',text='Убрать ответственого')],
                 [InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]

headman_menu = InlineKeyboardMarkup(inline_keyboard=headman_buttons)