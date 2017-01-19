#!/bin/bash

./pull.sh 2> /tmp/1.txt >>events.log
./get_scheduledevents.py
