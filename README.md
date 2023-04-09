Dart-Scoreboard

- sudo addgroup --system darts
- sudo adduser --disabled-password --system --home /var/lib/darts --gecos "Darts-scoreboard" --ingroup darts darts

- sudo mkdir /opt/darts && sudo chown darts:darts /opt/darts
- sudo -u darts git clone https://github.com/luukderooij/Dart-Scoreboard.git /opt/darts

- sudo cp -v /opt/darts/scripts/darts.service /etc/systemd/system/darts.service
- sudo chown root:root /etc/systemd/system/darts.service 
- sudo chmod 644 /etc/systemd/system/darts.service

- sudo apt install python3-pip sudo -u darts python3 -m pip install -r requirements.txt

- sudo systemctl enable darts
- sudo systemctl start darts
- sudo systemctl status darts