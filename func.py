import sqlite3
import threading

import telebot
from telebot import TeleBot

from config import BOT_TOKEN, ADMINS

connection = sqlite3.connect("fb_shop.db", check_same_thread=False)
local = threading.local()
bot = TeleBot(BOT_TOKEN)


def is_admin(user_id):
    return str(user_id) in ADMINS


def get_db_connection():
    if not hasattr(local, "connection"):
        local.connection = sqlite3.connect('fb_shop.db')
    return local.connection


def send_info_products(id: str, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"SELECT {info} FROM Products WHERE id = ?", (id,))
        result = c.fetchone()
        return result[0]


def changeinfo_products(id: str, name, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"UPDATE Products SET {name} = ? WHERE id = ?", (info, id))
        connection.commit()


def send_info_mini_category(id: str, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"SELECT {info} FROM Mini_Category WHERE id = ?", (id,))
        result = c.fetchone()
        return result[0]


def changeinfo_mini_category(id: str, name, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"UPDATE Mini_Category SET {name} = ? WHERE id = ?", (info, id))
        connection.commit()


def send_info_categories(id: str, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"SELECT {info} FROM Category WHERE id = ?", (id,))
        result = c.fetchone()
        return result[0]


def send_info_users(user_id: str, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"SELECT {info} FROM Users WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0]


def changeinfo_users(user_id: str, name, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"UPDATE Users SET {name} = ? WHERE user_id = ?", (info, user_id))
        connection.commit()


def changeinfo_categories(id: str, name, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"UPDATE Category SET {name} = ? WHERE id = ?", (info, id))
        connection.commit()


def send_info_control(id: str, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"SELECT {info} FROM Control_ids WHERE id = ?", (id,))
        result = c.fetchone()
        return result[0]


def changeinfo_control(id: str, name, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"UPDATE Control_ids SET {name} = ? WHERE id = ?", (info, id))
        connection.commit()

def get_user_by_id(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM Users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()


def get_individual_cabinet(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, bonuses, refferal FROM Users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        data = {"user_id": row[0], "bonuses": row[1], "refferal": row[2]}
        return data
    return None


def new_user_register(user_id: int, message):
    if get_user_by_id(user_id) == None:
        ref_link = f"https://t.me/FN_shopBot?start={message.chat.id}"
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Users (user_id, refferal) VALUES (?, ?)", (user_id, ref_link))
        connection.commit()
    else:
        print(f"Пользователь {user_id} уже существует")


def update_referral_bonuses(inviter_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE Users SET bonuses = COALESCE(bonuses, 0) + 1 WHERE user_id = ?", (inviter_id,))
    connection.commit()


def get_all_categories():
    cursor = connection.cursor()
    cursor.execute("SELECT id, category_name FROM Category")
    return cursor.fetchall()


def get_all_mini_categories():
    cursor = connection.cursor()
    cursor.execute("SELECT id, mini_category_name FROM Mini_Category")
    return cursor.fetchall()


def get_category_by_id(id):
    cursor = connection.cursor()
    cursor.execute("SELECT id, category_name FROM Category WHERE id = ?", (id,))
    category = cursor.fetchone()
    return category


def get_mini_category_by_id(id):
    cursor = connection.cursor()
    cursor.execute("SELECT id, mini_category_name FROM Mini_Category WHERE id = ?", (id,))
    category = cursor.fetchone()
    return category


def get_all_products_by_mini_category(mini_category_id):
    cursor = connection.cursor()
    cursor.execute("SELECT id, product_name, product_price, mini_category FROM Products WHERE mini_category = ?",
                   (mini_category_id,))
    return cursor.fetchall()


def get_all_mini_categories_by_category(category_id):
    cursor = connection.cursor()
    cursor.execute("SELECT id, mini_category_name, category FROM Mini_Category WHERE category = ?", (category_id,))
    return cursor.fetchall()


def get_product_by_id(id):
    cursor = connection.cursor()
    cursor.execute("SELECT id, product_name, product_price, category, verified"
                   " FROM Products WHERE id = ?", (id,))
    product = cursor.fetchone()
    return product


def get_all_products():
    cursor = connection.cursor()
    cursor.execute("SELECT id, product_name, verified FROM Products")
    return cursor.fetchall()


def delete_category(category_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Category WHERE id = ?", (category_id,))
    connection.commit()


def delete_product(product_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Products WHERE id = ?", (product_id,))
    connection.commit()


def save_new_category(message):
    category = message.text
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Category (category_name) VALUES (?)", (category,))
    connection.commit()
    bot.send_message(message.chat.id, "Категория успешно создана")


def get_all_user_ids():
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM Users")
    return cursor.fetchall()


def get_last_id():
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM Users ORDER BY id DESC LIMIT 1")

    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None


def save_new_card(message):
    card = message.text
    changeinfo_control(1, "card", card)

    bot.send_message(message.chat.id, "Карта успешно сохранена")


def create_request(message, user_id, product_id, username):
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_name = f'payment_images/{message.chat.id}_{message.message_id}.jpg'
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

    cursor = connection.cursor()
    cursor.execute("INSERT INTO Request (payment_image, user_id, product_id) VALUES (?, ?, ?)",
                   (str(file_name), user_id, product_id,))
    connection.commit()

    bot.send_message(message.chat.id, "Запрос на покупку успешно отправлен✅.\n\n"
                                      "После проверки вам напишут и выдадут товар. Ожидание может занять до 30минут")

    product_name = send_info_products(product_id, "product_name")
    product_price = send_info_products(product_id, "product_price")
    product_mini_category_id = send_info_products(product_id, "mini_category")
    product_category_id = send_info_mini_category(product_mini_category_id, "category")
    product_mini_category_name = send_info_mini_category(product_mini_category_id, "mini_category_name")
    product_category_name = send_info_categories(product_category_id, "category_name")

    with open(file_name, "rb") as img:
        bot.send_photo(5651185819, photo=img, caption=f"Вам пришел запрос на получение: {product_name} | "
                                                      f"{product_price}₽\n{product_category_name} | "
                                                      f"{product_mini_category_name}"
                                                      f"\n\nНикнейм Пользователя @{username}")


def create_request_bonus(message, user_id, product_id, username, bonus):
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_name = f'payment_images/{message.chat.id}_{message.message_id}.jpg'
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

    cursor = connection.cursor()
    cursor.execute("INSERT INTO Request (payment_image, user_id, product_id) VALUES (?, ?, ?)",
                   (str(file_name), user_id, product_id,))
    connection.commit()

    bot.send_message(message.chat.id, "Запрос на покупку успешно отправлен✅.\n\n"
                                      "После проверки вам напишут и выдадут товар. Ожидание может занять до 30минут")

    product_name = send_info_products(product_id, "product_name")
    product_price = send_info_products(product_id, "product_price")
    product_mini_category_id = send_info_products(product_id, "mini_category")
    product_category_id = send_info_mini_category(product_mini_category_id, "category")
    product_mini_category_name = send_info_mini_category(product_mini_category_id, "mini_category_name")
    product_category_name = send_info_categories(product_category_id, "category_name")
    bonus_price = product_price - bonus

    with open(file_name, "rb") as img:
        bot.send_photo(5651185819, photo=img, caption=f"Вам пришел запрос на получение: {product_name} | "
                                                      f"{bonus_price}(Бонусов {bonus})₽\n{product_category_name} | "
                                                      f"{product_mini_category_name}"
                                                      f"\n\nНикнейм Пользователя @{username}")



