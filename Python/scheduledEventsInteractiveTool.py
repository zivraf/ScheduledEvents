#!/usr/bin/python

import urllib.request
import json
import socket
import sys, getopt
import logging
from enum import Enum


metadata_url="http://169.254.169.254/metadata/latest/scheduledevents"
headers="{Metadata:true}"
this_host=socket.gethostname()
log_format = " %(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('example')
logging.basicConfig(format=log_format, level=logging.DEBUG)

class LogType(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERR = 3

def get_scheduled_events():
   """log_event (LogType.DEBUG, "get_scheduled_events was called ")"""
   logger.DEBUG ("get_scheduled_events was called")
   req=urllib.request.Request(metadata_url)
   req.add_header('Metadata','true')
   resp=urllib.request.urlopen(req)
   data=json.loads(resp.read().decode('utf8'))
   logger.DEBUG ("scheduled events: \n:"+data)
   return data

def ack_event(evt):
    """log_event (LogType.DEBUG, "ack_event was called with eventID "+ evt['EventId'])"""
    logger.INFO ("ack_event was called with eventID "+ evt['EventId'])
    ack_msg="{\"StartRequests\":[{\"EventId\":\""+evt['EventId'] +"\"}]}"
    res=urllib.urlopen("http://169.254.169.254/metadata/latest/scheduledevents", data=ack_msg).read()

def handle_scheduled_events(data):
    """log_event (LogType.DEBUG, "handle_scheduled_events was called with "+ str(len(data['Events']))) """
    logger.INFO ("handle_scheduled_events was called with "+ str(len(data['Events'])))

    for evt in data['Events']:
        eventid=evt['EventId']
        status=evt['EventStatus']
        resources=evt['Resources'][0]
        eventype=evt['EventType']
        restype=evt['ResourceType']
        notbefore=evt['NotBefore'].replace(" ","_")
        log_event (LogType.DEBUG, "EventId: "+ eventid+ " Type: "+ eventype+" Status: "+ status)
        if this_host in evt['Resources'][0]:
            """log_event (LogType.DEBUG, "THIS host is scheduled for " + eventype + " not before " + notbefore)"""
            logger.info ("THIS host is scheduled for " + eventype + " not before " + notbefore)
            userAck = input ('Are you looking to acknowledge the event (y/n)? ')
            if userAck == 'y':
                ack_event (evt)
            

def log_event (eventType,message):
    print (eventType.name + " : " +  message)

def main():
    """log_event (LogType.INFO, "Azure Scheduled Events Interactive Tool")"""
    logger.debug ("Azure Scheduled Events Interactive Tool")
    data=get_scheduled_events()
    handle_scheduled_events(data)


if __name__ == '__main__':
  main()
  sys.exit(0)
