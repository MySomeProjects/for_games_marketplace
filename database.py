import sqlite3


connection = sqlite3.connect("fb_shop.db")


def database_create_users():
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_id INTEGER UNIQUE NOT NULL,
    bonuses INTEGER DEFAULT 0,
    refferal TEXT UNIQUE
    )
    ''')

    connection.commit()


def database_create_category():
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Category (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    category_name TEXT NOT NULL,
    category_image TEXT,
    verified TEXT
    )
    ''')

    connection.commit()


def database_create_mini_category():
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mini_Category (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    mini_category_name TEXT,
    mini_category_image TEXT,
    category INTEGER,
    verified TEXT
    )''')

    connection.commit()


def database_create_products():
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    product_name TEXT,
    product_price REAL,
    product_image TEXT,
    category INTEGER,
    mini_category INTEGER,
    verified TEXT)
    ''')

    connection.commit()


def database_create_for_admin_ids():
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Control_ids (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_id INTEGER,
    telegram_user_id INTEGER,
    category_id INTEGER,
    product_id INTEGER,
    add_image TEXT,
    card INTEGER
    )''')

    connection.commit()


def database_create_buy_request():
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Request (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    payment_image TEXT,
    user_id INTEGER,
    product_id INTEGER
    )''')

    connection.commit()
