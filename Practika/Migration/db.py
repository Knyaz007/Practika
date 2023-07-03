# -*- coding: utf-8 -*-
import os
from alembic import context
import configparser
import sqlalchemy_class
import shutil

# Get the current module's file path
module_path = os.path.abspath(__file__)

# Get the directory containing the module file
module_directory = os.path.dirname(module_path)

# Construct the config_file path relative to the module directory
config_file = os.path.join(module_directory, "database_config.ini")


def read_database_config(file_path):
    config = configparser.RawConfigParser()
    config.read(file_path)
    database_config = {
        "username": config.get("database", "username"),
        "password": config.get("database", "password"),
        "host": config.get("database", "host"),
        "port": config.get("database", "port"),
        "database": config.get("database", "database"),
    }
    return database_config


def change_sqlalchemy_url(new_url):
    # Этот обновленный код создает временную копию alembic.ini файла,
    # изменяет sqlalchemy.url значение во временной копии с сохранением комментариев,
    # а затем заменяет исходный файл измененной копией.

    # Получение абсолютного пути к файлу go_migration.py
    file_path = os.path.abspath(__file__)

    # Получение пути к директории, содержащей файл go_migration.py
    directory = os.path.dirname(file_path)

    # Формирование пути к файлу alembic.ini
    config_path = os.path.join(directory, "alembic.ini")

    # Проверка существования файла alembic.ini
    if not os.path.exists(config_path):
        print(f"Config file '{config_path}' not found")
        return

    # Создание временной копии файла alembic.ini
    temp_config_path = os.path.join(directory, "alembic_temp.ini")
    shutil.copy2(config_path, temp_config_path)

    # Изменение значения sqlalchemy.url во временной копии
    with open(temp_config_path, 'r') as temp_config_file:
        lines = temp_config_file.readlines()

    with open(temp_config_path, 'w') as temp_config_file:
        for line in lines:
            if line.strip().startswith('sqlalchemy.url'):
                temp_config_file.write(f'sqlalchemy.url = {new_url}\n')
            else:
                temp_config_file.write(line)

    # Замена исходного файла alembic.ini временной копией
    shutil.move(temp_config_path, config_path)


database_config = read_database_config(config_file)
username = database_config["username"]
password = database_config["password"]
host = database_config["host"]
port = database_config["port"]
database = database_config["database"]


original_location = change_sqlalchemy_url(f"postgresql://{username}:{password}@{host}:{port}/{database}")

Base = sqlalchemy_class.Base
metadata = Base.metadata


def change_script_location(new_location):
    # Этот обновленный код создает временную копию alembic.ini файла,
    # изменяет script_location значение во временной копии с сохранением комментариев,
    # а затем заменяет исходный файл измененной копией.

    # Получение абсолютного пути к файлу go_migration.py
    file_path = os.path.abspath(__file__)

    # Получение пути к директории, содержащей файл go_migration.py
    directory = os.path.dirname(file_path)

    # Формирование пути к файлу alembic.ini
    config_path = os.path.join(directory, "alembic.ini")

    # Проверка существования файла alembic.ini
    if not os.path.exists(config_path):
        print(f"Config file '{config_path}' not found")
        return

    # Создание временной копии файла alembic.ini
    temp_config_path = os.path.join(directory, "alembic_temp.ini")
    shutil.copy2(config_path, temp_config_path)

    # Изменение значения script_location во временной копии
    with open(temp_config_path, 'r') as temp_config_file:
        lines = temp_config_file.readlines()

    with open(temp_config_path, 'w') as temp_config_file:
        for line in lines:
            if line.strip().startswith('script_location'):
                temp_config_file.write(f'script_location = {new_location}\n')
            else:
                temp_config_file.write(line)

    # Замена исходного файла alembic.ini временной копией
    shutil.move(temp_config_path, config_path)
