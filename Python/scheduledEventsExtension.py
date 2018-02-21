#!/usr/bin/python

import json
import socket
import sys, getopt
import logging
from enum import Enum
from datetime import datetime
import base64
import hmac
import hashlib
import time
import urllib.request
import urllib.parse
import configparser
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.eventgrid import EventGridManagementClient
from datetime import datetime
from azure.eventgrid import EventGridClient
from msrest.authentication import TopicCredentials
import requests

metadata_url="http://169.254.169.254/metadata/scheduledevents?api-version=2017-08-01"
headers="{Metadata:true}"
this_host=socket.gethostname()
log_format = " %(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('example')
logging.basicConfig(format=log_format, level=logging.DEBUG)


class EventGridMsgSender:
 
    def __init__(self, connectionString=None):
        if connectionString == None:
            config = configparser.ConfigParser()
            config.read('scheduledEventsExtensionConfig.ini')
            self.topicKey = config['DEFAULT']['topic_key']
            if self.topicKey is None:
                logger.error ("Failed to load Event Grid key. Make sure config file contains 'topic_key' entry")
            self.topicName = config['DEFAULT']['topic_name']
            if self.topicName is None:
                logger.error ("Failed to load Event Grid Topic Name. Make sure config file contains 'topic_name' entry")
            self.credentials = TopicCredentials(self.topicKey)
            self.egClient = EventGridClient(self.credentials)


    def send_to_evnt_grid (self, msgId, msg):
        logger.debug ("send_to_evnt_grid: MsgId: "+ msgId+", MsgData: "+ msg)
        self.egClient.publish_events(
            self.topicName,
            events=[{
            'id' : msgId,
            'subject' : "Scheduled Event",
            'data':  msg,
        'event_type': 'PersonalEventType',
        'event_time': datetime(2018, 1, 30),
        'data_version': 1
    }])
   

def send_to_event_grid (msgId, evt):
    logger.debug ("send_to_event_grid called with MsgId "+ msgId)
    egMsgSender = EventGridMsgSender()
    result=  egMsgSender.send_to_evnt_grid("1234-abc",scheduledEventMsg)
    logger.debug ("send_to_event_hub returned "+ result)


def get_scheduled_events():
   logger.debug ("get_scheduled_events was called")
   req=urllib.request.Request(metadata_url)
   req.add_header('Metadata','true')
   logger.debug ("Calling for scheduled events: "+ metadata_url)
   resp=urllib.request.urlopen(req)
   data=json.loads(resp.read().decode('utf8'))
   '''logger.debug ("scheduled events: \n:"+data)'''
   return data

def ack_event(evt):
    logger.info ("ack_event was called with eventID "+ evt['EventId'])
    ack_msg="{\"StartRequests\":[{\"EventId\":\""+evt['EventId'] +"\"}]}"
    ack_msg=ack_msg.encode()
    res=urllib.request.urlopen("http://169.254.169.254/metadata/scheduledevents?api-version=2017-08-01", data=ack_msg).read()
    #current_time = datetime.now().strftime('%H:%M:%S')
    #ehMsg = '{ "Hostname":"' + this_host+ '","Time":"'+current_time+'","LogType":"INFO","Msg":"Scheduled Event was acknowledged","EventID":"'+evt['EventId']+'"}'
    #send_to_event_hub(ehMsg)

def handle_scheduled_events(egMsgSender,data, autoApprove):
    logger.info ("handle_scheduled_events was called with "+ str(len(data['Events'])))
    if len(data['Events']) == 0:
        current_time = datetime.now().strftime('%H:%M:%S')
        ehMsg = '{ "Hostname":"' + this_host+ '","Time":"'+current_time+'","LogType":"DEBUG","Msg":"No Scheduled Events"}'
        logger.debug ("handle_scheduled_events: No Scheduled Events for host: " + this_host)
    
    for evt in data['Events']:
        logger.debug ("Handle a scheduled event")
        eventid=evt['EventId']
        status=evt['EventStatus']
        resources=evt['Resources'][0]
        eventype=evt['EventType']
        restype=evt['ResourceType']
        notbefore=evt['NotBefore'].replace(" ","_")
        logger.info ("EventId: "+ eventid+ " Type: "+ eventype+" Status: "+ status+" Resource: "+resources)

        current_time = datetime.now().strftime('%H:%M:%S')
        ehMsg = '{ "Hostname":"' + this_host+ '","Time":"'+current_time+'","Msg":"Scheduled Event was detected","EventID":"'+eventid+'","EventType":"'+eventype+'","Resource":"'+resources+'","NotBefore":"'+notbefore+'"}'
        logger.debug ("Event MSG: "+ehMsg)

        if this_host in evt['Resources'][0]:
            logger.debug ("About to send a message to event grid: " + ehMsg)
            result=  egMsgSender.send_to_evnt_grid(eventid,ehMsg)
            logger.info ("THIS host is scheduled for " + eventype + " not before " + notbefore)
            if autoApprove == True:
                logger.info ("APPROVE Scheduled Event for host " + this_host)    
                ack_event (evt)
            

def main():
    logger.debug ("Azure Scheduled Events Extension - START")
    egMsgSender = EventGridMsgSender()
    data=get_scheduled_events()
    handle_scheduled_events(egMsgSender,data,True)

    logger.debug ("Azure Scheduled Events Extension - FINISH")

 

if __name__ == '__main__':
  main()
  sys.exit(0)
