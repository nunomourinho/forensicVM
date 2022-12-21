call env_forensicvm\scripts\activate.bat
pyinstaller --noconfirm --onefile --console --icon "static\novnc\app\images\icons\favicon.ico" --clean --hidden-import django --add-data "app;app/" --add-data "conf;conf/" --add-data "static;static/" --add-data "templates;templates/" "manage.py"
move dist\manage.exe manage.exe
