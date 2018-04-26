#Install pip
pip install proxy.py

#!/bin/bash

# install python3, pip and Azre event grid client
apt-get -y update
apt-get install python3-pip python-dev build-essential -y
pip3 install azure-mgmt
pip3 install azure-mgmt-eventgrid

workserver_path=/srv/scheduledEvents
mkdir $workserver_path
cp scheduledEventsExtension.py $workserver_path
cp scheduledEventsExtensionConfig.ini $workserver_path
cp eventGridHelper.py $workserver_path
cp scheduledEventsHelper.py $workserver_path

# create a service
touch /etc/systemd/system/scheduledEvents.service
printf '[Unit]\nDescription=scheduled events extension\nAfter=rc-local.service\n' >> /etc/systemd/system/scheduledEvents.service
printf '[Service]\nWorkingDirectory=%s\n' $workserver_path >> /etc/systemd/system/scheduledEvents.service
printf 'ExecStart=/usr/bin/python3 %s/scheduledEventsExtension.py\n' $workserver_path >> /etc/systemd/system/scheduledEvents.service
printf 'ExecReload=/bin/kill -HUP $MAINPID\nKillMode=process\nRestart=on-failure\n' >> /etc/systemd/system/scheduledEvents.service
printf '[Install]\nWantedBy=multi-user.target\nAlias=scheduledEvents.service' >> /etc/systemd/system/scheduledEvents.service
chmod +x /etc/systemd/system/scheduledEvents.service

# start the  service
service scheduledEvents start


