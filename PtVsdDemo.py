
#!/usr/bin/python

import json
import urllib2
import socket
import sys
import ptvsd

ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))

#Enable the below line of code only if you want the application to wait untill the debugger has attached to it
ptvsd.wait_for_attach()

metadata_url="http://169.254.169.254/metadata/latest/scheduledevents?api-version=2017-08-01"
headers="{Metadata:true}"
this_host=socket.gethostname()

def get_scheduled_events():
   req=urllib2.Request(metadata_url)
   req.add_header('Metadata','true')
   resp=urllib2.urlopen(req)
   data=json.loads(resp.read())
   return data

def handle_scheduled_events(data):
    for evt in data['Events']:
        eventid=evt['EventId']
        status=evt['EventStatus']
        resources=evt['Resources'][0]
        eventype=evt['EventType']
        restype=evt['ResourceType']
        notbefore=evt['NotBefore'].replace(" ","_")
        if (this_host in evt['Resources'][0]) and (status == "Scheduled"):
            print "+ Scheduled Event. This host is scheduled for " + eventype + " not before " + notbefore
            print "++ Add you logic here"

def main():
   data=get_scheduled_events()
   handle_scheduled_events(data)
   

if __name__ == '__main__':
  main()
  sys.exit(0)

