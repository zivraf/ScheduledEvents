#!/bin/bash

message=`curl http://169.254.169.254/metadata/latest/scheduledevents` 
logger $message
echo $message
