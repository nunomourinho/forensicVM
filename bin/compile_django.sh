source /forensicVM/main/django-app/env_linux/bin/activate
python3 compile_django.py /forensicVM/main/django-app /forensicVM/setup/repo/forensic-vm-1.0/forensicVM/main
rsync -a /forensicVM/bin/ /forensicVM/setup/repo/forensic-vm-1.0/forensicVM/bin
rsync -a /forensicVM/usr/ /forensicVM/setup/repo/forensic-vm-1.0/forensicVM/usr
rsync -a /forensicVM/plugins/ /forensicVM/setup/repo/forensic-vm-1.0/forensicVM/plugins
rsync -a /forensicVM/main/django-app/env_linux/ /forensicVM/setup/repo/forensic-vm-1.0/forensicVM/main/env_linux

deactivate
