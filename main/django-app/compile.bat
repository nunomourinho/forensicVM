call env_forensicvm\scripts\activate.bat
pyinstaller --noconfirm --onefile --console --icon "static\novnc\app\images\icons\favicon.ico" --add-data "app;app/" --add-data "conf;conf/" --add-data "static;static/" --add-data "templates;templates/" --clean  "manage.py"
move dist\manage.exe manage.exe
rem --hidden-import django --hidden-import os   --paths env_forensicvm\scripts\Lib\site-packages 
