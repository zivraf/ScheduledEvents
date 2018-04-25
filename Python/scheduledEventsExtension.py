#!/usr/bin/python

# Scheduled Event Extension
import json
import socket
import sys, getopt
import logging
import time 
import datetime
import configparser
from enum import Enum
from datetime import datetime
import scheduledEventsHelper
import eventGridHelper

log_format = " %(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('ScheduledEvents')
logging.basicConfig(format=log_format, level=logging.DEBUG)
agentSection = 'AGENT'
eventGridSection= 'EVENT-GRID'

def main():
    logger.debug ("Azure Scheduled Events Extension")
    
    # load config file
    try: 
        config = configparser.ConfigParser()
        config.read('scheduledEventsExtensionConfig.ini')
    except:
        logger.error ("Failed to load configuration")

    autoAck = config.getboolean(agentSection,'scheduledEvents_autoAck')
    if autoAck is None:
        logger.debug ("Failed to configure auto ack , default to false")
        autoAck = False

    sampleFrequency = config.getint (agentSection,'agent_sampleFrequency')
    if sampleFrequency <1 or sampleFrequency > 60:
        logger.warn ("Failed to configure sample frequency , default to 5 minutes ")
        sampleFrequency = 300

    # Test Scheduled Events - need to run on an Azure VM
    seHelper = scheduledEventsHelper.ScheduledEventsHelper()

    isRunning = True
    egHelper = eventGridHelper.EventGridMsgSender()
    
    while (isRunning):
        try: 
            eventData = seHelper.get_scheduled_events()
        
            if eventData is None or len(eventData)==0 or len(eventData['Events']) == 0:
                logger.debug ("No Scheduled Events")
            else :
                seHelper.log_event(eventData)
                egHelper.send_to_evnt_grid(eventData)
                if autoAck :
                    # Ack the message - need to run on Azure VM
                    seHelper.ack_event(eventData)
                # stop the agent after the scheduled event was published
                isRunning = False
        except e:
            logger.error ("failed to retrieve scheduled events "+e)
            isRunning = False
        if (isRunning): 
            time.sleep(sampleFrequency)

    logger.debug (": Azure Scheduled Events Extension - COMPLETED ")

if __name__ == '__main__':
  main()
  sys.exit(0)
