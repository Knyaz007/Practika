from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,declarative_base


from alembic import context
import configparser

#config_file = "database_config.ini"
config_file = "C:\\Users\\Adminchik\\Desktop\\Practika\\Practika\\Migration\\database_config.ini"

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

database_config = read_database_config(config_file)
username = database_config["username"]
password = database_config["password"]
host = database_config["host"]
port = database_config["port"]
database = database_config["database"]

# Получение строки подключения из конфигурации
#SQLALCHEMY_DATABASE_URL = context.config.get_main_option("sqlalchemy.url")

# Далее можно использовать SQLALCHEMY_DATABASE_URL для создания подключения к базе данных


SQLALCHEMY_DATABASE_URL = "postgresql://student:1234@LocalHost:5432/practika2"

## Чтение параметров из текстового документа
#with open("path/to/file.txt", "r") as file:
#    lines = file.readlines()
#    username = lines[0].strip()
#    password = lines[1].strip()
#    host = lines[2].strip()
#    port = lines[3].strip()
#    database = lines[4].strip()

## Формирование строки подключения
#SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata
# Получение списка таблиц
table_names = metadata.tables.keys()

# Вывод имен таблиц
for table_name in table_names:
    print(table_name)