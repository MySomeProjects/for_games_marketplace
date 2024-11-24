from telebot import types
from func import is_admin


def start_menu(user_id):
    start_menu_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton(text="Главное меню📃")
    button2 = types.KeyboardButton(text="Поддержка👼")
    button3 = types.KeyboardButton(text="Админ Панель⌨️")

    start_menu_buttons.add(button1)
    start_menu_buttons.add(button2)

    if is_admin(user_id):
        start_menu_buttons.add(button3)

    return start_menu_buttons


def main_menu():
    main_menu_buttons = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="Личный Кабинет✍️", callback_data="individual_cabinet")
    button2 = types.InlineKeyboardButton(text="Товары🏪", callback_data="products")
    button3 = types.InlineKeyboardButton(text="Реферальная Система📩", callback_data="referral_system")
    button4 = types.InlineKeyboardButton(text="Отзывы✅", callback_data="reviews",
                                         url='https://t.me/otziviFN')

    main_menu_buttons.add(button1)
    main_menu_buttons.add(button2)
    main_menu_buttons.add(button3)
    main_menu_buttons.add(button4)

    return main_menu_buttons


def admin_menu():
    admin_menu_buttons = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text='Категории', callback_data='categories')
    button2 = types.InlineKeyboardButton(text="Разделы", callback_data="mini_categories")
    button3 = types.InlineKeyboardButton(text='Товары', callback_data='admin_products')
    button4 = types.InlineKeyboardButton(text='Рассылка', callback_data='add')
    button5 = types.InlineKeyboardButton(text='Пользователи', callback_data='users_count')
    button6 = types.InlineKeyboardButton(text='Карта', callback_data='card')

    admin_menu_buttons.add(button1, button2, button3)
    admin_menu_buttons.add(button4)
    admin_menu_buttons.add(button5)
    admin_menu_buttons.add(button6)

    return admin_menu_buttons


def add_path():
    add_path_buttons = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text='Рассылка с Картинкой', callback_data='add_with')
    button2 = types.InlineKeyboardButton(text="Рассылка без Картинки", callback_data="add_without")

    add_path_buttons.add(button1, button2)

    return add_path_buttons


# def categories():
#     categories_buttons = types.InlineKeyboardMarkup
