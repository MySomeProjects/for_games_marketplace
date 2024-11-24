import time

from telebot import TeleBot
import telebot

from keyboard import start_menu, main_menu, admin_menu, add_path
from database import (database_create_users, database_create_products, database_create_category,
                      database_create_for_admin_ids, database_create_mini_category, database_create_buy_request)
from func import new_user_register, get_individual_cabinet, get_user_by_id, update_referral_bonuses, \
    delete_category, get_all_products, save_new_category, get_category_by_id, get_all_categories, get_product_by_id, \
    delete_product, send_info_products, connection, changeinfo_products, \
    send_info_categories, changeinfo_control, send_info_control, send_info_users, \
    changeinfo_categories, get_all_mini_categories, send_info_mini_category, changeinfo_mini_category, \
    get_all_mini_categories_by_category, get_all_products_by_mini_category, get_mini_category_by_id, create_request, \
    changeinfo_users, create_request_bonus, get_all_user_ids, get_last_id, save_new_card, is_admin
from config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)

database_create_users()
database_create_category()
database_create_products()
database_create_for_admin_ids()
database_create_mini_category()
database_create_buy_request()


@bot.message_handler(commands=['start'])
def start(message):
    inviter_id = None
    if len(message.text.split()) > 1:
        inviter_id = int(message.text.split()[1])

    # Проверяем, есть ли пользователь в базе данных
    if get_user_by_id(message.chat.id) is None:

        if inviter_id:
            if get_user_by_id(inviter_id) is not None:
                update_referral_bonuses(inviter_id)
            else:
                print(f"Пригласивший пользователь с ID {inviter_id} не найден в базе данных.")  # Отладка

        new_user_register(message.chat.id, message)
    else:
        print(f"Пользователь {message.chat.id} уже существует в базе данных.")  # Отладочное сообщение

    bot.send_message(message.chat.id, f"Приветствую тебя {message.from_user.first_name}! Это магазин FH_Shop🏪.\n\n"
                                      f"Здесь ты найдешь все то что тебе поможет тебе сделать твой игровой процесс "
                                      f"приятнее и насыщеннее👼.\nИгровая валюта,Аккаунты,Подписки и многое другое📃.\n"
                                      f"Надеюсь ты найдешь то что тебе придется по вкусу.\n\n Приятной игры❤️",
                     reply_markup=start_menu(message.chat.id))


@bot.message_handler(func=lambda message: True)
def main_message_handlers(message):
    if message.text == "Главное меню📃":
        with open("images/IMG_20241105_074920_427.png", 'rb') as img:
            bot.send_photo(message.chat.id, photo=img, caption="Главное меню бота\n"
                                              "Это самый честный бот по доната и покупкам\n"
                                              "Наш канал https://t.me/FN_chik", reply_markup=main_menu())
    if message.text == "Админ Панель⌨️":
        if is_admin(message.chat.id):
            bot.send_message(message.chat.id, "Вы находитесь в панели Администратора", reply_markup=admin_menu())
        else:
            return


@bot.callback_query_handler(func=lambda call: True)
def main_callback_handlers(call):
    if call.data == "individual_cabinet":
        info = get_individual_cabinet(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        markup = telebot.types.InlineKeyboardMarkup()
        cancel = telebot.types.InlineKeyboardButton("Назад⬅️", callback_data="cancel_to_menu")
        markup.add(cancel)

        if info:
            bonuses = info['bonuses'] if info['bonuses'] is not None else 0  # Заменяем None на 0
            with open("images/IMG_20241105_074921_167.png", 'rb') as img:
                bot.send_photo(
                    call.message.chat.id,
                    photo=img,
                    caption=f"Ваш личный кабинет:\n\n"
                    f"Ваш User ID: {info['user_id']}\nВаши Бонусы: {bonuses}",
                    reply_markup=markup
                )
        else:
            bot.send_message(call.message.chat.id, "Информация о личном кабинете не найдена.")

    if call.data == "products":
        categories = get_all_categories()
        markup = telebot.types.InlineKeyboardMarkup()

        for category_id, name in categories:
            markup.add(telebot.types.InlineKeyboardButton(text=name, callback_data=f"category_{category_id}"))

        markup.add(telebot.types.InlineKeyboardButton(text="Назад ⬅️", callback_data="cancel_to_menu"))

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберите интересующую вас Категорию", reply_markup=markup)

    if call.data == "referral_system":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = telebot.types.InlineKeyboardMarkup()
        cancel = telebot.types.InlineKeyboardButton("Назад⬅️", callback_data="cancel_to_menu")
        markup.add(cancel)
        info = get_individual_cabinet(call.message.chat.id)
        if info:
            bot.send_message(call.message.chat.id, f"Ваша реферальная ссылка:\n{info['refferal']}\nПриглашайте людей"
                                                   f" и получайте БОНУСЫ!!!", reply_markup=markup)

    if call.data == "add":
        bot.send_message(call.message.chat.id, "Отправьте изображение:")
        bot.register_next_step_handler(call.message, lambda message: step_for_add_with(message))

    # elif call.data == "add_without":
    #     bot.send_message(call.message.chat.id, "Отправьте Текст:")
    #     bot.register_next_step_handler(call.message, lambda message: step_for_add_without(message))

    elif call.data == "users_count":
        last_id = get_last_id()
        bot.send_message(call.message.chat.id, f"Всего в боте {last_id} пользователей")

    elif call.data == "categories":
        categories = get_all_categories()
        markup = telebot.types.InlineKeyboardMarkup()

        for category_id, name in categories:
            markup.add(telebot.types.InlineKeyboardButton(text=name, callback_data=f"admin_category_{category_id}"))

        markup.add(telebot.types.InlineKeyboardButton(text='Добавить Категорию', callback_data='add_category'))

        bot.send_message(call.message.chat.id, "Выберите категорию:", reply_markup=markup)

    elif call.data == "mini_categories":
        mini_categories = get_all_mini_categories()
        markup = telebot.types.InlineKeyboardMarkup()

        for mini_category_id, name in mini_categories:
            verified = send_info_mini_category(mini_category_id, "verified")
            if verified == "True":
                markup.add(telebot.types.InlineKeyboardButton(text=name,
                                                              callback_data=f"admin_mini_category_{mini_category_id}"))

        markup.add(telebot.types.InlineKeyboardButton(text='Добавить Раздел', callback_data='add_mini_category'))

        bot.send_message(call.message.chat.id, "Выберите Раздел:", reply_markup=markup)

    elif call.data == 'add_category':
        bot.send_message(call.message.chat.id, "Напишите название категории:")
        bot.register_next_step_handler(call.message, lambda message: save_new_category(message))

    elif call.data == 'add_products':
        bot.send_message(call.message.chat.id, "Напишите название Продукта:")
        bot.register_next_step_handler(call.message, lambda message: step_1_for_new_product(message))

    elif call.data == "add_mini_category":
        bot.send_message(call.message.chat.id, "Напишите название Раздела:")
        bot.register_next_step_handler(call.message, lambda message: step_1_for_new_mini_category(message))

    elif call.data == "admin_products":
        products = get_all_products()
        markup = telebot.types.InlineKeyboardMarkup()

        # Добавляем кнопки для каждого проверенного продукта
        for product_id, product_name, verified in products:
            if verified == "True":
                markup.add(
                    telebot.types.InlineKeyboardButton(text=product_name, callback_data=f"products_{product_id}"))

        # Добавляем кнопку для добавления нового продукта
        markup.add(telebot.types.InlineKeyboardButton(text='Добавить Продукт', callback_data='add_products'))

        # Отправляем сообщение с клавиатурой
        bot.send_message(call.message.chat.id, "Выберите Продукт:", reply_markup=markup)

    elif call.data == "card":
        bot.send_message(call.message.chat.id, "Введите новую карту:")
        bot.register_next_step_handler(call.message, lambda message: save_new_card(message))

    elif call.data.startswith("admin_category_"):
        category_id = int(call.data.split("_")[1])

        category = get_category_by_id(category_id)

        if category:
            id, category_name = category

            delete_markup = telebot.types.InlineKeyboardMarkup()
            delete_markup.add(telebot.types.InlineKeyboardButton("Удалить", callback_data=f"delete_category_{category_id}"))

            bot.send_message(
                call.message.chat.id,
                f"ID Категории: {category_id}\nНазвание Категории: {category_name}",
                reply_markup=delete_markup
            )
        else:
            bot.send_message(call.message.chat.id, "Категория не найдена.")

    elif call.data.startswith("admin_mini_category_"):
        mini_category_id = int(call.data.split("_")[3])

        category = get_mini_category_by_id(mini_category_id)

        if category:
            id, category_name = category

            photo = send_info_mini_category(mini_category_id, "mini_category_image")
            get_category_id = send_info_mini_category(mini_category_id, "category")
            category_id = send_info_categories(get_category_id, "category_name")

            delete_markup = telebot.types.InlineKeyboardMarkup()
            delete_markup.add(telebot.types.InlineKeyboardButton("Удалить", callback_data=f"delete_mini_category_{mini_category_id}"))

            with open(f"{photo}", 'rb') as img:
                bot.send_photo(
                    call.message.chat.id,
                    photo=img,
                    caption=f"ID Раздела: {mini_category_id}\nНазвание Раздела: {category_name}\n"
                            f"Категория Раздела: {category_id}",
                    reply_markup=delete_markup
                )
        else:
            bot.send_message(call.message.chat.id, "Категория не найдена.")

    elif call.data.startswith("products_"):
        product_id = int(call.data.split("_")[1])
        bot.delete_message(call.message.chat.id, call.message.message_id)

        product = get_product_by_id(product_id)

        if product:

            product_name = send_info_products(product_id, "product_name")

            delete_markup = telebot.types.InlineKeyboardMarkup()
            delete_markup.add(telebot.types.InlineKeyboardButton("Удалить", callback_data=f"delete_product_{product_id}"))

            bot.send_message(
                call.message.chat.id,
                f"ID Продукта: {product_id}\nНазвание Продукта: {product_name}",
                reply_markup=delete_markup
            )
        else:
            bot.send_message(call.message.chat.id, "Продукт не найден.")

    elif call.data.startswith("categories_"):
        category_id = int(call.data.split("_")[1])
        mini_category_id = send_info_control(1, "category_id")

        # Сохраняем выбор категории в базе данных
        changeinfo_mini_category(mini_category_id, "category", category_id)

        # Получаем информацию о продукте для подтверждения
        mini_category_name = send_info_mini_category(mini_category_id, "mini_category_name")
        mini_category_image = send_info_mini_category(mini_category_id, "mini_category_image")
        category = send_info_categories(category_id, "category_name")

        # Подтверждение
        apply_markup = telebot.types.InlineKeyboardMarkup()
        yes = telebot.types.InlineKeyboardButton("Подтвердить", callback_data=f"yes3_{mini_category_id}")
        no = telebot.types.InlineKeyboardButton("Отмена", callback_data=f"no3_{mini_category_id}")
        apply_markup.add(yes, no)

        with open(f"{mini_category_image}", 'rb') as img:
            bot.send_photo(
                call.message.chat.id,
                photo=img,
                caption=f"Подтвердите/Отклоните создание Раздела\n\nНазвание Раздела: {mini_category_name}\n"
                f"\nКатегория Раздела: {category}",
                reply_markup=apply_markup
            )

    elif call.data.startswith("mini_categories_"):
        category_id = int(call.data.split("_")[2])
        product_id = send_info_control(1, "product_id")

        # Сохраняем выбор категории в базе данных
        changeinfo_products(product_id, "mini_category", category_id)

        # Получаем информацию о продукте для подтверждения
        product_name = send_info_products(product_id, "product_name")
        product_price = send_info_products(product_id, "product_price")
        category = send_info_mini_category(category_id, "mini_category_name")

        # Подтверждение
        apply_markup = telebot.types.InlineKeyboardMarkup()
        yes = telebot.types.InlineKeyboardButton("Подтвердить", callback_data=f"yes_{product_id}")
        no = telebot.types.InlineKeyboardButton("Отмена", callback_data=f"no_{product_id}")
        apply_markup.add(yes, no)

        bot.send_message(
            call.message.chat.id,
            f"Подтвердите/Отклоните создание Товара\n\nНазвание Товара: {product_name}\n"
            f"Цена Товара: {product_price}\n"
            f"\nКатегория Раздела: {category}",
            reply_markup=apply_markup
        )

    elif call.data.startswith("adds_yes_"):
        text = str(call.data.split("_")[2])
        adds_image = send_info_control(1, "add_image")
        user_ids = get_all_user_ids()

        for user_id in user_ids:
            print(user_id)
            try:
                with open(adds_image, "rb") as img:
                    bot.send_photo(user_id, photo=img, caption=text)
                time.sleep(0.5)  # Задержка между отправкой сообщений
            except telebot.apihelper.ApiException as e:
                # Проверяем, заблокировал ли пользователь бота
                if "blocked" in str(e):
                    print(f"Пользователь {user_id} заблокировал бота. Пропускаем.")
                else:
                    print(f"Ошибка при отправке пользователю {user_id}: {e}")

    elif call.data.startswith("adds_yeswithout_"):
        text = str(call.data.split("_")[2])
        user_ids = get_all_user_ids()

        for user_id in user_ids:
            print(user_id)
            print(text)
            try:
                bot.send_message(user_id, text)
                time.sleep(0.5)
            except telebot.apihelper.ApiException as e:
                if "blocked" in str(e):
                    print(f"Пользователь {user_id} заблокировал бота. Пропускаем.")
                else:
                    print(f"Ошибка при отправке пользователю {user_id}: {e}")

    elif call.data == "adds_no":
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data.startswith("category_"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        category_id = int(call.data.split("_")[1])
        mini_categories = get_all_mini_categories_by_category(category_id)
        markup = telebot.types.InlineKeyboardMarkup()
        category_name = send_info_categories(category_id, "category_name")

        for mini_category_id, mini_category_name, category in mini_categories:
            verified = send_info_mini_category(mini_category_id, "verified")
            if verified == "True":
                markup.add(telebot.types.InlineKeyboardButton(text=mini_category_name,
                                                              callback_data=f"mini_category_{mini_category_id}"))

        markup.add(telebot.types.InlineKeyboardButton(text="Назад⬅️️", callback_data="products"))

        bot.send_message(call.message.chat.id, f"Разделы Из Категории {category_name}", reply_markup=markup)

    elif call.data.startswith("mini_category_"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        mini_category_id = int(call.data.split("_")[2])
        products = get_all_products_by_mini_category(mini_category_id)
        markup = telebot.types.InlineKeyboardMarkup()
        category_name = send_info_mini_category(mini_category_id, "mini_category_name")
        mini_category_image = send_info_mini_category(mini_category_id, "mini_category_image")

        for product_id, product_name, product_price, category in products:
            verified = send_info_products(product_id, "verified")
            if verified == "True":
                markup.add(telebot.types.InlineKeyboardButton(text=f"{product_name} | {product_price}₽",
                                                              callback_data=f"product_{product_id}"))

        markup.add(telebot.types.InlineKeyboardButton(text="Назад⬅️️", callback_data="products"))

        with open(f'{mini_category_image}', 'rb') as img:
            bot.send_photo(call.message.chat.id, photo=img,
                           caption=f"Товары из Раздела: {category_name}", reply_markup=markup)

    elif call.data.startswith("product_"):
        product_id = int(call.data.split("_")[1])
        bot.delete_message(call.message.chat.id, call.message.message_id)

        product = get_product_by_id(product_id)

        if product:

            product_name = send_info_products(product_id, "product_name")
            mini_category_id = send_info_products(product_id, "mini_category")
            mini_category_name = send_info_mini_category(mini_category_id, "mini_category_name")
            category_id = send_info_mini_category(mini_category_id, "category")
            category_name = send_info_categories(category_id, "category_name")
            product_price = send_info_products(product_id, "product_price")

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("Купить🛍️", callback_data=f"buy_product_{product_id}"))
            markup.add(telebot.types.InlineKeyboardButton("Назад⬅️", callback_data=f"products"))

            bot.send_message(
                call.message.chat.id,
                f"Категория Товара: {category_name} | {mini_category_name}"
                f"\nНазвание Товара: {product_name}\nЦена: {product_price}\n",
                reply_markup=markup
            )
        else:
            bot.send_message(call.message.chat.id, "Продукт не найден.")

    elif call.data.startswith("buy_product_"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        product_id = int(call.data.split("_")[2])
        user_info = bot.get_chat(call.message.chat.id)
        username = user_info.username

        product_name = send_info_products(product_id, "product_name")
        product_price = send_info_products(product_id, "product_price")

        card = send_info_control(1, "card")

        bonuses = send_info_users(call.message.chat.id, "bonuses")
        if bonuses is None:
            bonuses = 0  # Устанавливаем значение 0, если бонусы отсутствуют

        bonus_markup = telebot.types.InlineKeyboardMarkup()
        bonus_markup.add(telebot.types.InlineKeyboardButton("Да✅", callback_data=f"bonus_yes_{product_id}"))
        bonus_markup.add(telebot.types.InlineKeyboardButton("Нет❌", callback_data=f"bonus_no_{product_id}"))

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Подтвердить✅', callback_data=f"apply_product_buy_{product_id}"))

        if bonuses > 0:
            bot.send_message(call.message.chat.id, f"На вашем счету есть {bonuses} бонусов. Хотите ими "
                                                   f"воспользоваться?", reply_markup=bonus_markup)
        else:
            # Обработка покупки без бонусов
            if username is None:
                bot.send_message(call.message.chat.id,
                                 "Перед покупкой установите себе телеграм Никнейм, чтобы мы могли с вами связаться")
                return
            else:
                bot.send_message(call.message.chat.id, f"Для покупки {product_name} переведите сумму в размере "
                                                       f"{product_price}₽ по номеру карты, отправленному ниже.\n"
                                                       f"Нажмите кнопку Подтвердить✅ и отправьте скриншот перевода")
                bot.send_message(call.message.chat.id, f"{card}", reply_markup=markup)

    elif call.data.startswith("bonus_yes_"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        product_id = int(call.data.split("_")[2])

        # Получаем информацию о продукте и пользователе
        product_name = send_info_products(product_id, "product_name")
        product_price = send_info_products(product_id, "product_price")
        card = send_info_control(1, "card")
        user_info = bot.get_chat(call.message.chat.id)
        username = user_info.username

        bonuses = send_info_users(call.message.chat.id, "bonuses")

        bonus_price = product_price - bonuses

        apply_bonus_markup = telebot.types.InlineKeyboardMarkup()
        apply_bonus_markup.add(telebot.types.InlineKeyboardButton('Подтвердить✅',
                                                                  callback_data=f"apply_product_bonus_{product_id}"))

        if username is None:
            bot.send_message(call.message.chat.id,
                             "Перед покупкой установите себе телеграм Никнейм, чтобы мы могли с вами связаться")
            return
        else:
            bot.send_message(call.message.chat.id,
                             f"Для покупки {product_name} переведите сумму в размере {bonus_price}"
                             f"₽ по номеру карты отправленному ниже.\n"
                             f"Нажмите кнопку Подтвердить✅ и отправьте скриншот перевода")

            bot.send_message(call.message.chat.id, f"{card}", reply_markup=apply_bonus_markup)

    elif call.data.startswith("bonus_no_"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        card = send_info_control(1, "card")
        product_id = int(call.data.split("_")[2])
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Подтвердить✅', callback_data=f"apply_product_buy_{product_id}"))
        product_name = send_info_products(product_id, "product_name")
        product_price = send_info_products(product_id, "product_price")
        user_info = bot.get_chat(call.message.chat.id)
        username = user_info.username
        if username is None:
            bot.send_message(call.message.chat.id, "Перед покупкой установите себе телеграм Никнейм что мы бы"
                                                   "мы смогли с вами связаться")
            return
        else:
            bot.send_message(call.message.chat.id, f"Для покупки {product_name} переведите сумму в размере "
                                                   f"{product_price}₽ по номеру карты отправленному ниже.\n"
                                                   f"нажмите кнопку Подтвердить✅ и отправьте скриншот перевода")
            bot.send_message(call.message.chat.id, f"{card}", reply_markup=markup)

    elif call.data.startswith("apply_product_buy_"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        product_id = int(call.data.split("_")[3])
        user_info = bot.get_chat(call.message.chat.id)
        username = user_info.username

        if username is None:
            bot.send_message(call.message.chat.id, "Перед подтверждением установите себе телеграм Никнейм что мы бы"
                                                   "мы смогли с вами связаться")
        else:
            bot.send_message(call.message.chat.id, "Отправьте Скриншот перевода")
            bot.register_next_step_handler(call.message, lambda message: create_request(message=message,
                                                                                        user_id=call.message.chat.id,
                                                                                        product_id=product_id,
                                                                                        username=username,
                                                                                        ))

    elif call.data.startswith("apply_product_bonus_"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        product_id = int(call.data.split("_")[3])
        user_info = bot.get_chat(call.message.chat.id)
        username = user_info.username

        bonuses = send_info_users(call.message.chat.id, "bonuses")
        changeinfo_users(call.message.chat.id, "bonuses", 0)

        if username is None:
            bot.send_message(call.message.chat.id, "Перед подтверждением установите себе телеграм Никнейм что мы бы"
                                                   "мы смогли с вами связаться")
        else:
            bot.send_message(call.message.chat.id, "Отправьте Скриншот перевода")
            bot.register_next_step_handler(call.message, lambda message: create_request_bonus(message=message,
                                                                                        user_id=call.message.chat.id,
                                                                                        product_id=product_id,
                                                                                        username=username,
                                                                                        bonus=bonuses))

    elif call.data.startswith("yes_"):
        product_id = int(call.data.split("_")[1])
        changeinfo_products(product_id, "verified", "True")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Вы успешно добавили товар")

    elif call.data.startswith("no_"):
        product_id = int(call.data.split("_")[1])
        changeinfo_products(product_id, "verified", "False")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Вы отменили добавление товара")

    elif call.data.startswith("yes3_"):
        mini_category_id = int(call.data.split("_")[1])
        changeinfo_mini_category(mini_category_id, "verified", "True")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Вы успешно добавили Раздел")

    elif call.data.startswith("no3_"):
        mini_category_id = int(call.data.split("_")[1])
        changeinfo_mini_category(mini_category_id, "verified", "False")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Вы отменили добавление Раздела")

    elif call.data.startswith("delete_category_"):
        # Получаем ID категории для удаления
        category_id = int(call.data.split("_")[2])
        delete_category(category_id)
        bot.send_message(call.message.chat.id, "Категория удалена.", reply_markup=admin_menu())

    elif call.data.startswith("delete_product_"):
        # Получаем ID категории для удаления
        product_id = int(call.data.split("_")[2])
        delete_product(product_id)
        bot.send_message(call.message.chat.id, "Продукт удален.", reply_markup=admin_menu())

    elif call.data == 'cancel_to_menu':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Главное Меню:", reply_markup=main_menu())


def step_1_for_new_product(message):
    product = message.text
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Products (product_name) VALUES (?)", (product,))
    connection.commit()
    product_id = cursor.lastrowid
    changeinfo_control(1, "product_id", product_id)
    bot.send_message(message.chat.id, "Напишите цену товара:")
    bot.register_next_step_handler(message, lambda message: step_2_for_new_product(message, product_id))


def step_2_for_new_product(message, product_id):
    mini_categories = get_all_mini_categories()
    markup = telebot.types.InlineKeyboardMarkup()

    for mini_category_id, mini_category_name in mini_categories:
        verified = send_info_mini_category(mini_category_id, "verified")
        if verified == "True":
            markup.add(telebot.types.InlineKeyboardButton(text=mini_category_name,
                                                          callback_data=f"mini_categories_{mini_category_id}"))

    product_price = float(message.text)
    changeinfo_products(product_id, "product_price", product_price)
    bot.send_message(message.chat.id, "Выберите раздел товаров:", reply_markup=markup)


def step_1_for_new_mini_category(message):
    mini_category = message.text
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Mini_Category (mini_category_name) VALUES (?)", (mini_category,))
    connection.commit()
    mini_category_id = cursor.lastrowid
    changeinfo_control(1, "category_id", mini_category_id)
    bot.send_message(message.chat.id, "Отправьте Изображение к Разделу:")
    bot.register_next_step_handler(message, lambda message: step_2_for_new_mini_category(message, mini_category_id))


def step_2_for_new_mini_category(message, mini_category_id):
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        categories = get_all_categories()
        markup = telebot.types.InlineKeyboardMarkup()

        file_name = f'images/{message.chat.id}_{message.message_id}.jpg'
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        changeinfo_mini_category(mini_category_id, 'mini_category_image', str(file_name))


        for category_id, name in categories:
            markup.add(telebot.types.InlineKeyboardButton(text=name, callback_data=f"categories_{category_id}"))

        bot.send_message(message.chat.id, "Выберите категорию раздела:", reply_markup=markup)


def step_for_add_with(message):
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_name = f'adds_images/{message.chat.id}_{message.message_id}.jpg'
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        changeinfo_control(1, 'add_image', str(file_name))

        bot.send_message(message.chat.id, "Отправьте текст Объявления")
        bot.register_next_step_handler(message, lambda message: step_for_add_with_2(message))


def step_for_add_with_2(message):
    add_text = message.text
    add_image = send_info_control(1, "add_image")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Отправить✅", callback_data=f"adds_yes_{add_text}"))
    markup.add(telebot.types.InlineKeyboardButton("Отмена❌", callback_data="adds_no"))

    with open(add_image, "rb") as img:
        bot.send_photo(message.chat.id, photo=img, caption=add_text, reply_markup=markup)


def step_for_add_without(message):
    add_text = message.text

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Отправить✅", callback_data=f"adds_yeswithout_{add_text}"))
    markup.add(telebot.types.InlineKeyboardButton("Отмена❌", callback_data="adds_no"))

    bot.send_message(message.chat.id, add_text, reply_markup=markup)



bot.polling()