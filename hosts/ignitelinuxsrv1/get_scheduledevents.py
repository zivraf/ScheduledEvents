#!/usr/bin/python

import urllib,json
import urllib2
import sys

url="http://169.254.169.254/metadata/latest/scheduledevents"
#url="http://127.0.0.1/index.json"
existingEvents=urllib.urlopen('http://104.40.23.39/map.php?cmd=get&key=events')
events=json.loads(existingEvents.read())

response=urllib.urlopen(url)
data=json.loads(response.read())
for evt in data['Events']:
 eventid=evt['EventId']
 status=evt['EventStatus']
 resources=evt['Resources'][0]
 eventype=evt['EventType']
 restype=evt['ResourceType']
 notbefore=evt['NotBefore'].replace(" ","_")
 msg=restype+"_"+resources+"_"+status+"_"+eventype+"_Not_Before_"+notbefore
 if eventid not in events['data']:
   msg=msg+"_"+eventid
   urllib2.urlopen("http://104.40.23.39/map.php?cmd=set&key=events&value="+msg).read()
   print msg

sys.exit(0)
