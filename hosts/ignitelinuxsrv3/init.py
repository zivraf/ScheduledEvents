#!/usr/bin/python

import urllib,json
import urllib2
import socket
import sys


url="http://104.40.23.39/app.php"
this_host=socket.gethostname()
mr_url="http://169.254.169.254/metadata/latest/scheduledevents"
#mr_url="http://127.0.0.1/index.json"
#check if host can be set as active. check if no upcoming events
response=urllib.urlopen(mr_url)
data=json.loads(response.read())
update_topology=""
host_found_in_events="false"
response=urllib2.urlopen(url+"?cmd=get&key=topology")
array=response.read().split('@')

for evt in data['Events']:
  if this_host in evt['Resources'][0]:
    host_found_in_events="true"
    for host in array:
       if this_host in host:
          host=this_host+"=not_active"
       update_topology+=host+"@"
    break


if host_found_in_events=="false":
  for host in array:
    if this_host in host:
      host=this_host+"=active"
    update_topology+=host+"@"

urllib2.urlopen(url+"?cmd=set&key=topology&value="+update_topology).read()
