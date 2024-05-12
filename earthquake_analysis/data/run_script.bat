@echo off

echo Activating virtual environment
call ..\..\venv\Scripts\activate

cd ..

echo Running Django shell
python manage.py shell -c "exec(open('data\save_data_to_database.py').read())"

pause
