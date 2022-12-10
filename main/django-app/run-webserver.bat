set original_dir=%CD%
set venv_root_dir="%CD%\env_forensicvm"
cd %venv_root_dir%
call %venv_root_dir%\Scripts\activate.bat

cd %original_dir%
python manage.py runserver

call %venv_root_dir%\Scripts\deactivate.bat
cd %original_dir%
exit /B 1