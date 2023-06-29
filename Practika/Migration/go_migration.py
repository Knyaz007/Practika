from alembic import command
from alembic.config import Config






import os
from alembic import command
from alembic.config import Config

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
    # ������������ ���� � ���������� � ����������
    # ������������ ���� � ���������� � ����������
    migration_directory = os.path.join(directory, "alembic", "versions")


    # �������� ������������ Alembic �� ����� alembic.ini
    alembic_config = Config(config_path)


    ### ��������� ���� � ���������� � ����������
    alembic_config.set_main_option("version_locations", migration_directory)

     # ��������� �������� ���� version_locations
    version_locations = alembic_config.get_main_option("version_locations")

    print(f" version_locations: {version_locations}")

    ## �������� ������������ Alembic �� ����� alembic.ini
    #alembic_config = Config("alembic.ini")

    # ���������� ���� ������������� ��������
    command.upgrade(alembic_config, "head")

     




