dpkg --get-selections > ./package.list
mkdir ./sources.list
sudo cp -R /etc/apt/sources.list* ./sources.list/
sudo apt-key exportall > ./repo.keys
