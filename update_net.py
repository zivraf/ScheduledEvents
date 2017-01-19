#!/usr/bin/python

import json
import urllib2
import sys

metadata_url="http://169.254.169.254/metadata/latest/instance/network?format=json"
headers="{Metadata:true}"

controller_url="http://net_controller/map.php"

def get_net_metadata():
   req=urllib2.Request(metadata_url)
   req.add_header('Metadata','true')
   resp=urllib2.urlopen(req)
   data=json.loads(resp.read())
   return data

def parse_net_metadata(data):
   for item in data['interface']:
      macaddr=item['mac']
      fqdns_arr=item['idnsfqdn']
      routes_arr=item['ipv4']['routes']
      subnet_arr=item['ipv4']['subnet']
      ipv4_addr_arr=item['ipv4']['ipaddress']

def get_ipv4_addr(data):
   ip_list=[]
   for item in data['interface']:
     for i in range(len(item['ipv4']['ipaddress'])):
       ip_list.append(item['ipv4']['ipaddress'][i]['ipaddress'])
   return ip_list
     
def notify_controller(ip_list):
   print ip_list
   resp=urllib2.urlopen(controller_url+"?cmd=set&key=ipaddr&value="+str(ip_list)).read()

def main():
   ipv4_addr=[]
   data=get_net_metadata()
   ipv4_addr=get_ipv4_addr(data)
   notify_controller(ipv4_addr)
   

if __name__ == '__main__':
  main()
  sys.exit(0)
