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
from datetime import datetime
# import urllib.request
# import urllib.parse
# import requests

import configparser
from azure.eventgrid import EventGridClient
from msrest.authentication import TopicCredentials

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


log_format = " %(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('ScheduledEvents')
logging.basicConfig(format=log_format, level=logging.DEBUG)
eventGridSection= 'EVENT-GRID'
agentSection = 'AGENT'

class EventGridMsgSender:
     
    def __init__(self, connectionString=None):
        if connectionString == None:
            config = configparser.ConfigParser()
            config.read('scheduledEventsExtensionConfig.ini')
            self.topicKey = config.get(eventGridSection,'topic_key')
            if self.topicKey is None:
                logger.error ("Failed to load Event Grid key. Make sure config file contains 'topic_key' entry")
            self.topicEndpoint = config.get(eventGridSection,'topic_endpoint')
            if self.topicEndpoint is None:
                logger.error ("Failed to load Event Grid Topic Name. Make sure config file contains 'topic_name' entry")            
            self.credentials = TopicCredentials(self.topicKey)
            self.egClient = EventGridClient(self.credentials)
            self.handleLocalEventsOnly = config.getboolean(agentSection,'scheduledEvents_handleLocalOnly')
            if self.handleLocalEventsOnly is None:
                logger.debug ("Failed to load Event Grid Topic Name. Make sure config file contains 'topic_name' entry")
                self.handleLocalEventsOnly = False

    def send_to_evnt_grid (self, msg, localHostName):
        if len(msg['Events']) == 0:
            logger.debug ("send_to_evnt_grid: No Scheduled Events")
            return
        try:            
            logger.debug ("send_to_evnt_grid was called")
            credentials = TopicCredentials(self.topicKey)
            egClient = EventGridClient(credentials)
            
            for event in msg['Events']:
                eventid=event['EventId']
                status=event['EventStatus']
                eventype=event['EventType']
                restype=event['ResourceType']
                notbefore=event['NotBefore'].replace(" ","_")
                isLocal = False 
                for resourceId in event['Resources']:            
                    if localHostName in resourceId or self.handleLocalEventsOnly == False:
                        logger.debug ("before sending to event grid "+ str(datetime.now()))
                        self.egClient.publish_events(
                            self.topicEndpoint,
                            events=[{
                                'id' : eventid,
                                'subject' : "ScheduledEvent:"+eventype+", Host:"+resourceId+", Not Before:"+notbefore,
                                'data': event,
                                'event_type': "ScheduledEvent",
                                'event_time': datetime.now(),
                                'data_version': "1.0"
                                }] )
                        logger.debug ("send_to_evnt_grid: message "+eventid+" was send to EventGrid")
                    
        except:
            logger.error ("send_to_evnt_grid: failed to send ")
