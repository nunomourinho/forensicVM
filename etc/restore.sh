apt-key add ./repo.keys
cp -R ~/sources.list* /etc/apt/
apt-get update
apt-get install dselect
dpkg --set-selections < ./package.list
dselect
