from aiogram.types import (InlineKeyboardButton,InlineKeyboardMarkup)

super_admin_buttons = [[InlineKeyboardButton(callback_data='admin_list',text='Список администраторов')],
                      [InlineKeyboardButton(callback_data='headman_list',text='Список старост')],
                      [InlineKeyboardButton(callback_data='add_admin',text='Добавить администратора')],
                      [InlineKeyboardButton(callback_data='delete_admin',text='Удалить администратора')],
                      [InlineKeyboardButton(callback_data='add_headman',text='Добавить старосту')],
                      [InlineKeyboardButton(callback_data='delete_headman',text='Удалить старосту')],
                      [InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]
                    
super_admin_menu = InlineKeyboardMarkup(inline_keyboard=super_admin_buttons)

admin_buttons = [[InlineKeyboardButton(callback_data='admin_list',text='Список администраторов')],
                      [InlineKeyboardButton(callback_data='headman_list',text='Список старост')],
                      [InlineKeyboardButton(callback_data='add_headman',text='Добавить старосту')],
                      [InlineKeyboardButton(callback_data='delete_headman',text='Удалить старосту')],
                      [InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]

admin_menu = InlineKeyboardMarkup(inline_keyboard=admin_buttons)

headman_buttons = [[InlineKeyboardButton(callback_data='responsible_list',text='Список помощников'),],
                 [InlineKeyboardButton(callback_data='classmates_list',text='Список одноклассников')],
                 [InlineKeyboardButton(callback_data='add_new_resposible',text='Добавить помощника')],
                 [InlineKeyboardButton(callback_data='delete_resposible',text='Убрать помощника')],
                 [InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]

headman_menu = InlineKeyboardMarkup(inline_keyboard=headman_buttons)