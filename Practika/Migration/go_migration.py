from alembic import command
from alembic.config import Config






import os
from alembic import command
from alembic.config import Config



import os
from alembic import command
from alembic.config import Config
from configparser import ConfigParser



import shutil

import shutil

def change_script_location2(new_location):
   # Этот обновленный код создает временную копию alembic.ini файла,
   #изменяет script_location значение во временной копии с сохранением комментариев, 
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
    #  Изменениев  файле параметра  script_location = Migration/alembic
    original_location = change_script_location2("Migration/alembic")
    
    # Формирование пути к директории с миграциями
    migration_directory = os.path.join(directory, "alembic", "versions")


    # Загрузка конфигурации Alembic из файла alembic.ini
    alembic_config = Config(config_path)


    ### Установка пути к директории с миграциями
    alembic_config.set_main_option("version_locations", migration_directory)

     # Получение значения поля version_locations
    version_locations = alembic_config.get_main_option("version_locations")

    print(f" version_locations: {version_locations}")

   
    # Применение всех непримененных миграций
    command.upgrade(alembic_config, "head")

    #  Изменениев  файле параметра  script_location = alembic
    original_location = change_script_location2("alembic")
     



