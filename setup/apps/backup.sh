dpkg --get-selections > ./package.list
dpkg --get-selections | awk '{print $1}' > ../installed_packages.txt
mkdir ./sources.list
sudo cp -R /etc/apt/sources.list* ./sources.list/
sudo apt-key exportall > ./repo.keys
