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
   # ���� ����������� ��� ������� ��������� ����� alembic.ini �����,
   #�������� script_location �������� �� ��������� ����� � ����������� ������������, 
   # � ����� �������� �������� ���� ���������� ������.




    # ��������� ����������� ���� � ����� go_migration.py
    file_path = os.path.abspath(__file__)

    # ��������� ���� � ����������, ���������� ���� go_migration.py
    directory = os.path.dirname(file_path)

    # ������������ ���� � ����� alembic.ini
    config_path = os.path.join(directory, "alembic.ini")

    # �������� ������������� ����� alembic.ini
    if not os.path.exists(config_path):
        print(f"Config file '{config_path}' not found")
        return

    # �������� ��������� ����� ����� alembic.ini
    temp_config_path = os.path.join(directory, "alembic_temp.ini")
    shutil.copy2(config_path, temp_config_path)

    # ��������� �������� script_location �� ��������� �����
    with open(temp_config_path, 'r') as temp_config_file:
        lines = temp_config_file.readlines()

    with open(temp_config_path, 'w') as temp_config_file:
        for line in lines:
            if line.strip().startswith('script_location'):
                temp_config_file.write(f'script_location = {new_location}\n')
            else:
                temp_config_file.write(line)

    # ������ ��������� ����� alembic.ini ��������� ������
    shutil.move(temp_config_path, config_path)
    

# ��������� ����������� ���� � ����� go_migration.py
file_path = os.path.abspath(__file__)

# ��������� ���� � ����������, ���������� ���� go_migration.py
directory = os.path.dirname(file_path)

# ������������ ���� � ����� alembic.ini
config_path = os.path.join(directory, "alembic.ini")

# �������� ������������� ����� alembic.ini
if not os.path.exists(config_path):
    print(f"Config file '{config_path}' not found")
else:
    #  ����������  ����� ���������  script_location = Migration/alembic
    original_location = change_script_location2("Migration/alembic")
    
    # ������������ ���� � ���������� � ����������
    migration_directory = os.path.join(directory, "alembic", "versions")


    # �������� ������������ Alembic �� ����� alembic.ini
    alembic_config = Config(config_path)


    ### ��������� ���� � ���������� � ����������
    alembic_config.set_main_option("version_locations", migration_directory)

     # ��������� �������� ���� version_locations
    version_locations = alembic_config.get_main_option("version_locations")

    print(f" version_locations: {version_locations}")

   
    # ���������� ���� ������������� ��������
    command.upgrade(alembic_config, "head")

    #  ����������  ����� ���������  script_location = alembic
    original_location = change_script_location2("alembic")
     



