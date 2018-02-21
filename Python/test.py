import configparser
config = configparser.ConfigParser()
config['TEST'] = {'topic_key': 'yNHvcAWiEXTbg2VnN7EhsVqdbfHPnAd7U7WBFj8snK8=',\
   'topic_name': 'scheduledeventdemoeg.eastus2euap-1.eventgrid.azure.net'}
with open('example.ini', 'w') as configfile:
   config.write(configfile)
