#!/bin/bash

cd /

sudo apt-get update
sudo apt-get install -y python3-dev
pip3 install -U pyrogram

pip3 install -U TgCrypto
pip3 install -U persiantools
pip3 install -U qrcode

pip3 install -U reportlab
pip3 install -U qrcode

sudo apt-get install -y libsqlite3-dev
sudo apt install build-essential

if ! command -v python3 &> /dev/null; then
    echo "Python not found. Installing..."
    sudo apt-get install -y python3
fi

if ! command -v git &> /dev/null; then
    echo "Git not found. Installing..."
    sudo apt-get install -y git
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found. Installing..."
    sudo apt-get install -y python3-pip
fi

if [ -d "SJbotbot" ]; then
    echo "Removing existing SJbotbeta directory..."
    rm -rf SJbotbot
fi

if [ -d "SJbotbeta" ]; then
    echo "Removing existing SJbotbeta directory..."
    rm -rf SJbotbeta
fi

if [ -d "SJbot" ]; then
    echo "Removing existing SJbot directory..."
    rm -rf SJbot
fi

if ps aux | grep -v grep | grep "python3 SJbot.py" &> /dev/null; then
    echo "Stopping existing SJbot process..."
    pkill -f "python3 SJbot.py"
fi

if ps aux | grep -v grep | grep "python3 SJbotbeta.py" &> /dev/null; then
    echo "Stopping existing SJbot process..."
    pkill -f "python3 SJbotbeta.py"
fi

if ps aux | grep -v grep | grep "python3 node_status_checker.py" &> /dev/null; then
    echo "Stopping existing node_status_checker process..."
    pkill -f "python3 node_status_checker.py"
fi

if ps aux | grep -v grep | grep "python3 monitoringbeta.py" &> /dev/null; then
    echo "Stopping existing monitoringbeta process..."
    pkill -f "python3 monitoringbeta.py"
fi

if ps aux | grep -v grep | grep "python3 monitoring.py" &> /dev/null; then
    echo "Stopping existing monitoring process..."
    pkill -f "python3 monitoring.py"
fi

if ps aux | grep -v grep | grep "python3 expired.py" &> /dev/null; then
    echo "Stopping existing expired process..."
    pkill -f "python3 expired.py"
fi

if ps aux | grep -v grep | grep "python3 limiteder.py" &> /dev/null; then
    echo "Stopping existing limiteder process..."
    pkill -f "python3 limiteder.py"
fi

rm -rf ./SJbot
cd /
mkdir ./SJbot
cd ./SJbot

git clone https://github.com/Denumen/SJbot.git .

sudo apt install -y python3.10-venv
python3 -m venv hold
source hold/bin/activate

pip install -U pyrogram tgcrypto requests Pillow qrcode[pil] persiantools pytz python-dateutil pysqlite3 cdifflib reportlab subprocess
sudo apt-get install sqlite3

read -p "Please enter name (nickname) : " name
read -p "Please enter telegram chatid : " chatid
read -p "Please enter telegram bot token: " token
read -p "Please enter panel sudo username : " user
read -p "Please enter panel sudo password : " password
read -p "Please enter panel domain (like: sub.domian.com:port) : " domain
read -p "Do you have SSL? (y/n): " ssl_response

#name='mehdi'
#chatid='5038952647'
#token='6995765932:AAEkdyVKQOY8cT_zHApRH567hxb-_uAdkdU'
#user='dfg392gt'
#password='q31Kt1H3r3N2'
#domain='feed.farsroid.tech:2087'

if [[ $ssl_response == "y" ]]; then
    domain="https://$domain"
else
    domain="http://$domain"
fi

sqlite3 /SJbot/SJbot.db <<EOF
CREATE TABLE bot
    (chatid INTEGER PRIMARY KEY,
     token TEXT);

CREATE TABLE monitoring
    (chatid INTEGER PRIMARY KEY,
     status TEXT,
     check_normal INTEGER,
     check_error INTEGER);

CREATE TABLE templates
    (name TEXT PRIMARY KEY,
     data INTEGER,
     date INTEGER,
     proxies TEXT,
     inbounds TEXT,
     price INTEGER);

CREATE TABLE accounts
    (chatid INTEGER PRIMARY KEY,
     username TEXT);

CREATE TABLE starters
    (chatid INTEGER PRIMARY KEY,
     customerid INTEGER);

CREATE TABLE users
    (chatid INTEGER PRIMARY KEY,
     role TEXT,
     name TEXT,
     username TEXT,
     password TEXT,
     domain TEXT,
     step TEXT,
     credit INTEGER);

CREATE TABLE IF NOT EXISTS messages
    (chatid INTEGER PRIMARY KEY,
    status TEXT);

INSERT INTO messages (chatid, status) VALUES ('$chatid', 'off');
INSERT INTO users (chatid, role, name, username, password, domain, step, credit) VALUES ('$chatid', 'boss', '$name', '$user', '$password', '$domain', 'None', '0');
INSERT INTO monitoring (chatid, status, check_normal, check_error) VALUES ('$chatid', 'on', '10', '100');
INSERT INTO bot (chatid, token) VALUES ("$chatid", "$token");
INSERT INTO accounts (chatid, username) VALUES ("$chatid", "dummybot");
INSERT INTO starters (chatid, customerid) VALUES ("$chatid", "867");
EOF

chmod +x monitoring.py
chmod +x SJbot.py
chmod +x expired.py
chmod +x limiteder.py
nohup python3 monitoring.py & disown
#nohup python3 SJbot.py & disown
nohup python3 expired.py & disown
nohup python3 limiteder.py & disown
chmod +x restart.sh
#cronjob="@reboot sleep 20 && /bin/bash /SJbotbot/restart.sh"
#if ! crontab -l | grep -Fq "$cronjob"; then
#  (crontab -l 2>/dev/null; echo "$cronjob") | crontab -
#fi

echo "SJbotbot is run!"
