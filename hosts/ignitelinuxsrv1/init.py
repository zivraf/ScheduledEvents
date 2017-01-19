#!/usr/bin/python

import urllib,json
import urllib2
import socket
import sys


url="http://104.40.23.39/app.php"
this_host=socket.gethostname()
mr_url="http://169.254.169.254/metadata/latest/scheduledevents"
mr_url="http://127.0.0.1/doc.json"
#check if host can be set as active. check if no upcoming events
response=urllib.urlopen(mr_url)
data=json.loads(response.read())
update_topology=""
host_found_in_events="false"
response=urllib2.urlopen(url+"?cmd=get&key=topology")
array=response.read().split('@')
doc_inc=data['DocumentIncarnation']
for evt in data['Events']:
  if this_host in evt['Resources'][0]:
    eventid=evt['EventId']
    host_found_in_events="true" 
    for host in array:    
       if this_host in host:
          if "active" in host:
            host=this_host+"=pending_reboot"
 	    break
          if "pending_reboot" in host:
            host=this_host+"=graceful_shutdown_in_progress"
 	    break
          if "graceful_shutdown" in host:
            host=this_host+"=closing_remaining_transactions"
 	    break
          if "closing_remaining_transactions" in host:
            host=this_host+"=acknowledging_the_event" 
 	    break
          if "acknowledging_the_event" in host:
            host=this_host+"=not_active"
 	    break
    update_topology+=host+"@"

if not data['Events']:
 for host in array:
  if this_host in host:
   host=this_host+"=active"
   update_topology+=host+"@"
#populate the rest of the topology
for host in array:
 if this_host not in host:
   print host
   update_topology+=host+"@"  

print update_topology
urllib2.urlopen(url+"?cmd=set&key=topology&value="+update_topology).read()

if host_found_in_events=="true" and eventid:
  ack_msg="{\"DocumentIncarnation\":"+str(doc_inc)+",\"StartRequests\":[{\"EventId\":\""+eventid+"\"}]}"
  res=urllib2.urlopen("http://169.254.169.254/metadata/latest/scheduledevents", data=ack_msg).read()
sys.exit(0)
