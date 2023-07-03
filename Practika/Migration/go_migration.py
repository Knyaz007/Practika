from alembic import command
from alembic.config import Config
from configparser import ConfigParser
import os
import shutil
import db

# Получение абсолютного пути к файлу go_migration.py
file_path = os.path.abspath(__file__)

# Получение пути к директории, содержащей файл go_migration.py
directory = os.path.dirname(file_path)

# Формирование пути к файлу alembic.ini
config_path = os.path.join(directory, "alembic.ini")

# Проверка существования файла alembic.ini
if not os.path.exists(config_path):
    print(f"Config file '{config_path}' not found")
else:

    script_location = os.path.join(directory, "alembic")

    # Изменение файла параметра script_location = Migration/alembic
    #original_location = db.change_script_location("Migration/alembic")

    # Формирование пути к директории с миграциями
    migration_directory = os.path.join(directory, "alembic", "versions")

    # Загрузка конфигурации Alembic из файла alembic.ini
    alembic_config = Config(config_path)

    # Установка пути к директории с миграциями
    alembic_config.set_main_option("version_locations", migration_directory)

    # Установка пути к криптам  
    alembic_config.set_main_option("script_location", script_location)

    # Получение значения поля version_locations
    version_locations = alembic_config.get_main_option("version_locations")
    print(f" version_locations: {version_locations}")

     # Получение значения поля script_location
    script_location = alembic_config.get_main_option("script_location")
    print(f" version_locations: {script_location}")

    ## Изменение параметра sqlalchemy.url
    #original_location = db.change_sqlalchemy_url(f"postgresql://{db.username}:{db.password}@{db.host}:{db.port}/{db.database}")

    # Создание новой миграции
    command.revision(alembic_config, autogenerate=True, message="New migration")

    # Применение всех непримененных миграций
    command.upgrade(alembic_config, "head")

    # Изменение файла параметра script_location = alembic
    original_location = db.change_script_location("alembic")
