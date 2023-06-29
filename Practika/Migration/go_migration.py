from alembic import command
from alembic.config import Config






import os
from alembic import command
from alembic.config import Config

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
    # Формирование пути к директории с миграциями
    # Формирование пути к директории с миграциями
    migration_directory = os.path.join(directory, "alembic", "versions")


    # Загрузка конфигурации Alembic из файла alembic.ini
    alembic_config = Config(config_path)


    ### Установка пути к директории с миграциями
    alembic_config.set_main_option("version_locations", migration_directory)

     # Получение значения поля version_locations
    version_locations = alembic_config.get_main_option("version_locations")

    print(f" version_locations: {version_locations}")

    ## Загрузка конфигурации Alembic из файла alembic.ini
    #alembic_config = Config("alembic.ini")

    # Применение всех непримененных миграций
    command.upgrade(alembic_config, "head")

     




