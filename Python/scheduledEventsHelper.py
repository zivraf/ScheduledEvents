#!/usr/bin/python

# Scheduled Event Helper utility 

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

# import urllib.request
# import urllib.parse

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


metadata_url="http://169.254.169.254/metadata/scheduledevents?api-version=2017-03-01"
headers="{Metadata:true}"
this_host=socket.gethostname()
log_format = " %(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('ScheduledEvents')
logging.basicConfig(format=log_format, level=logging.DEBUG)

class ScheduledEventsHelper:

    def get_scheduled_events(self):
        logger.debug ("get_scheduled_events was called")
        try: 
            req=Request(metadata_url)
            req.add_header('Metadata','true')                    
        except Exception:
            logger.warn ("get_scheduled_events: failed to set a request ")
                    
        try:
            resp=urlopen(req)
            data=json.loads(resp.read().decode('utf8'))            
        except:
            logger.warn ("get_scheduled_events: No instance metadata . Are you runnign an AZURE VM ? ")
            return        
        return data

    def ack_event(self,evt):
        for event in evt['Events']:
            isLocal = False
            for resourceId in event['Resources']:            
                if this_host in resourceId:
                    logger.info ("ack_event was called with eventID "+ event['EventId'])
                    ack_msg="{\"StartRequests\":[{\"EventId\":\""+event['EventId'] +"\"}]}"
                    ack_msg=ack_msg.encode()
                    res=urlopen(metadata_url, data=ack_msg).read()
                
    def log_event (self,evt):
        logger.info ("log_event was called")
        if len(evt['Events']) == 0:
            logger.info ("No Scheduled Events")
            return

        for event in evt['Events']:
            eventid=event['EventId']
            status=event['EventStatus']
            eventype=event['EventType']
            restype=event['ResourceType']
            notbefore=event['NotBefore'].replace(" ","_")
            isLocal = False
            for resourceId in event['Resources']:            
                if this_host in resourceId:
                    isLocal = True 

            logger.info ("EventId: "+ eventid+ " Type: "+ eventype+" Status: "+ status+ " isLocal: "+ str(isLocal))