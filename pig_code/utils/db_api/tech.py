import random

import mysql.connector

from .user import User
from .connection import Connection
from ...core import *
from ...core.config import users_schema, shop_schema, promo_code_schema, guilds_schema


class Tech:

    @staticmethod
    def create_user_table():
        columns = [
            'id varchar(32) PRIMARY KEY UNIQUE',
            'money int DEFAULT 0',
            "pig json",
            "inventory json",
            "stats json",
            "events json",
            "language varchar(10) DEFAULT 'en'",
            'premium boolean DEFAULT FALSE',
            'blocked boolean DEFAULT FALSE',
            'blocked_promocodes boolean DEFAULT FALSE',
            "block_reason varchar(1000) DEFAULT ''"
        ]
        try:
            Connection.make_request(f"CREATE TABLE {users_schema} ({columns[0]})", commit=False)
        except mysql.connector.errors.ProgrammingError:
            pass
        for column in columns[1:]:
            try:
                Connection.make_request(f"ALTER TABLE {users_schema} ADD COLUMN {column}", commit=False)
            except Exception as e:
                pass
                # print(e)

    @staticmethod
    def create_shop_table():
        columns = ['id int AUTO_INCREMENT PRIMARY KEY UNIQUE',
                   'update_timestamp varchar(32)',
                   'static_shop json',
                   'daily_shop json'
                   ]
        try:
            Connection.make_request(f"CREATE TABLE {shop_schema} ({columns[0]})", commit=False)
        except mysql.connector.errors.ProgrammingError:
            pass
        for column in columns[1:]:
            try:
                Connection.make_request(f"ALTER TABLE {shop_schema} ADD COLUMN {column}", commit=False)
            except:
                pass

    @staticmethod
    def create_promo_code_table():
        columns = ['id varchar(32) PRIMARY KEY UNIQUE',
                   'created varchar(32)',
                   'users_used json',
                   'max_uses int',
                   'prise json',
                   'expires_in int',
                   'can_use varchar(32)',
                   ]
        try:
            Connection.make_request(f"CREATE TABLE {promo_code_schema} ({columns[0]})", commit=False)
        except mysql.connector.errors.ProgrammingError:
            pass
        for column in columns[1:]:
            try:
                Connection.make_request(f"ALTER TABLE {promo_code_schema} ADD COLUMN {column}", commit=False)
            except:
                pass

    @staticmethod
    def create_guild_table():
        columns = ['id varchar(32) PRIMARY KEY UNIQUE',
                   'joined int',
                   'settings json',
                   ]
        try:
            Connection.make_request(f"CREATE TABLE {guilds_schema} ({columns[0]})", commit=False)
        except mysql.connector.errors.ProgrammingError:
            pass
        for column in columns[1:]:
            try:
                Connection.make_request(f"ALTER TABLE {guilds_schema} ADD COLUMN {column}", commit=False)
            except:
                pass

    @staticmethod
    def get_all_users():
        id_list = []
        connection = Connection.connect()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {users_schema}")
            results = cursor.fetchall()
            for i in results:
                id_list.append(i[0])
        return id_list

    @staticmethod
    def get_all_guilds():
        id_list = []
        connection = Connection.connect()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {guilds_schema}")
            results = cursor.fetchall()
            for i in results:
                id_list.append(i[0])
        return id_list
