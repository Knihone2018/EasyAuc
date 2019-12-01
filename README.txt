

sudo docker run --name Item -e MYSQL_ROOT_PASSWORD=123456 -p 9000:9000 -p 9100:3306 -d mysql:latest

sudo docker exec -it Item bash

apt-get update
apt-get install -y vim
apt-get install -y net-tools
apt-get install -y openssh-client
apt-get install -y python3-pip

pip3 install mysql-connector-python flask flask_cors pika uuid

mkdir -p /src/app
mkdir -p /src/photo
sudo docker cp item.py Item:/src/app
sudo docker cp client.py Item:/src/app

sudo docker commit Item easyauc:item
sudo docker save easyauc:item > item.tar
docker load < item.tar
sudo docker run --name Item -e MYSQL_ROOT_PASSWORD=123456 -p 9000:9000 -p 9100:3306 -d easyauc:item
