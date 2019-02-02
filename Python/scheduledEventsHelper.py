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

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

imds_url="http://169.254.169.254/metadata/instance?api-version=2017-08-01"
imds_headers="{Metadata:true}"
metadata_url="http://169.254.169.254/metadata/scheduledevents?api-version=2017-11-01"
headers="{Metadata:true}"
log_format = " %(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('ScheduledEvents')
logging.basicConfig(format=log_format, level=logging.DEBUG)
imds_data = "none"

class ScheduledEventsHelper:

    def get_scheduled_events(self):
        logger.debug ("get_scheduled_events was called")
        try: 
            req=Request(metadata_url)
            req.add_header('Metadata','true')   
        except Exception:
            logger.debug ("get_scheduled_events: failed to set a request ")
                    
        try:                 
            resp=urlopen(req)
            scheduledEvent_data=json.loads(resp.read().decode('utf8'))            
        except :
            logger.warn ("get_scheduled_events: failed to extract scheduled events . Are you running in AZURE? ")
            return        
        return scheduledEvent_data

    def get_imds_local_host(self):
        logger.warn ("get_imds_local_host was called")
        # Call IMDS to identify the host name
        try: 
            imds_req=Request(imds_url)
            imds_req.add_header('Metadata','true')                    
        except Exception:
            logger.debug ("get_imds_local_host: failed to set a request ")
                    
        try:
            imds_resp=urlopen(imds_req)
            imds_data=json.loads(imds_resp.read().decode('utf8'))            
        except:
            logger.warn ("get_imds_local_host: No instance metadata . Are you running an AZURE VM ? ")
        
        logger.debug ("get_imds_local_host: IMDS hostname is "+imds_data["compute"]["name"])
        return imds_data["compute"]["name"]

    def is_local_event (self,evt,localHostName):
        logger.warn ("is_local_event was called")
        
        isLocal = False
        for event in evt['Events']:
            for resourceId in event['Resources']:            
                logger.debug ("is_local_event: compare with resource in event: "+resourceId)

                if localHostName in resourceId:
                    logger.info ("ack_event was called on local host with eventID "+ event['EventId'])
                    isLocal = True

        return isLocal
        
    def ack_event(self,evt):
        for event in evt['Events']:
            for resourceId in event['Resources']:            
                if imds_data["compute"]["name"] in resourceId:
                    logger.info ("ack_event was called on local host with eventID "+ event['EventId'])
                    ack_msg="{\"StartRequests\":[{\"EventId\":\""+event['EventId'] +"\"}]}"
                    ack_msg=ack_msg.encode()
                    res=urlopen(metadata_url, data=ack_msg).read()
                    return True
        return False
                
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

            logger.info ("EventId: "+ eventid+ " Type: "+ eventype+" Status: "+ status)
