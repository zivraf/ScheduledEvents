# ScheduledEventsExtension - In-VM notification extension for Azure Virtual Machines using Serverless
## About Azure scheduled events
What if you could learn about upcoming events which may impact the availability of your VM and plan accordingly? With Azure Scheduled Events you can.

Scheduled Events is one of the subservices under Azure Metadata Service that surfaces information regarding upcoming events (for example, reboot). Scheduled Events give your application sufficient time to perform preventive tasks to minimize the effect of such events. Scheduled events are surfaced using a REST Endpoint from within the VM, and the information is made available via a Non-routable IP so that it is not exposed outside the VM.

more on scheduled events :  [Azure Scheduled Events documentation for Windows](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/scheduled-events), or [Linux](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/scheduled-events)

## Why Serverless 
Since Azure scheduled events are surfaced within the VM, they are best for auto response like saving state, proactive failover etc.. Still, there are cases where we wish to respond to a scheduled evnent from outside the VM. These responses include any forwarding, notification and alerting steps where we would like a human to get involved or trigger a response by anothe rplatform. 
For that, we have the Azure serverless offerings which include Azure Functions and Logic Apps.
Azure Event Grid is a fully-managed intelligent event routing service that allows for uniform event consumption using a publish-subscribe model. 

## The Scheduled Event Extension
This extension monitors for scheduled events (frequency is set in the .ini file). Once identified, it publishes the event using event grid.  

## Deploying the extention
In order to deploy andrun the extnesion follow these steps:
1. Create an [Event-Grid] (https://docs.microsoft.com/en-us/azure/event-grid/)
2. Pick the topic end point which should look like this <yourname>.<region>-1.eventgrid.azure.net. [**Note that the portal adds some prefix and postfix to th eend point name**]
2. Launch the extension from [here] (https://github.com/zivraf/ScheduledEvents/tree/master/setup/linux) or just follow the link below. Identify the VM you wish to add this extension to and the topic endpoint and SAS key

(You can check whether the code was deploy and run in your vm. Look for the directory /srv/scheduledEvents and a new service scheduledEvents)

3. Write a sample Logic App triggered fro mthe event grid topic
4. Test the experience E2E by initiating a VM reboot fro mthe portal 

<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fzivraf%2FScheduledEvents%2Fmaster%2Fsetup%2Flinux%2Fazuredeploy.json" target="_blank">
    <img src="http://azuredeploy.net/deploybutton.png"/>
    </a>
