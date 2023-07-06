cd.. 
cd..


rem Установка зависимостей (если нужно)
poetry install

rem Вывод информации о виртуальной среде
poetry env info

rem Обновление зависимостей (если нужно)
poetry update

rem Запуск модуля
python Practika\Migration\go_migration.py

pause