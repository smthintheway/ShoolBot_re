from aiogram.types import (InlineKeyboardButton,InlineKeyboardMarkup)

back_button = [[InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]
Back_keyboard = InlineKeyboardMarkup(inline_keyboard=back_button)

Binary_choose = [[InlineKeyboardButton(callback_data='yes',text='Да'),
                  InlineKeyboardButton(callback_data='no',text='Нет')],
                 [InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]
Binary_keyboard = InlineKeyboardMarkup(inline_keyboard=Binary_choose)

Arrows = [[InlineKeyboardButton(callback_data='back',text='<-'),InlineKeyboardButton(callback_data='next',text='->')],
          [InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]
Arrows_keyboard = InlineKeyboardMarkup(inline_keyboard=Arrows)

Edit_ask = [[InlineKeyboardButton(callback_data='edit',text='Изменить'),
             InlineKeyboardButton(callback_data='ask',text='Уточнить')],
            [InlineKeyboardButton(callback_data='back_to_menu',text='Назад')]]
Edit_ask_keyboard = InlineKeyboardMarkup(inline_keyboard=Edit_ask)

Types = [[InlineKeyboardButton(text='Текст', callback_data= 'text'),
          InlineKeyboardButton(text='Фото', callback_data='photo'),
          InlineKeyboardButton(text="Документ",callback_data='document')]]
Types_keyboard = InlineKeyboardMarkup(inline_keyboard=Types)

Menu_button = [[InlineKeyboardButton(callback_data='back_to_menu',text='Меню')]]
Menu_button_keyboard = InlineKeyboardMarkup(inline_keyboard=Menu_button)
