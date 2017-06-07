# Set up the scheduled events URI for a VNET-enabled VM
$localHostIP = "169.254.169.254"
$scheduledEventURI = 'http://{0}/metadata/scheduledevents?api-version=2017-03-01' -f $localHostIP 
$eventSource = "AzureScheduledEvents" 
$eventLogName = "Application"
$eventLogId = 1234   

# How to get scheduled events 
function GetScheduledEvents($uri)
{
    $scheduledEvents = Invoke-RestMethod -Headers @{"Metadata"="true"} -URI $uri -Method get
    $json = ConvertTo-Json $scheduledEvents
    Write-Host "Received following events: `n" $json
    return $scheduledEvents
}

# How to approve a scheduled event
function ApproveScheduledEvent($eventId, $docIncarnation, $uri)
{    
    # Create the Scheduled Events Approval Document
    $startRequests = [array]@{"EventId" = $eventId}
    $scheduledEventsApproval = @{"StartRequests" = $startRequests; "DocumentIncarnation" = $docIncarnation} 

    # Convert to JSON string
    $approvalString = ConvertTo-Json $scheduledEventsApproval

    Write-Host "Approving with the following: `n" $approvalString

    # Post approval string to scheduled events endpoint
    Invoke-RestMethod -Uri $uri -Headers @{"Metadata"="true"} -Method POST -Body $approvalString
}

function HandleScheduledEvents($scheduledEvents)
{
    foreach($event in $scheduledEvents.Events)
    {
        $str = "*" +$event.EventId +"*"
        if (Get-EventLog -LogName $eventLogName -Source $eventSource -Message $str)
        {
             # Event is already logged 
        }
        else
        {
            Write-EventLog -LogName Application -Source $eventSource -EventId $eventLogId -EntryType  Information -Message $event] 
        }
    }
}

######### Sample Scheduled Events Interaction #########
if(!(Get-Eventlog -LogName $eventLogName -Source $eventSource)){
     $ErrorActionPreference = "Continue"
     try {
          New-Eventlog -LogName $eventLogName  -Source $eventSource | Out-Null
          Write-EventLog -LogName $eventLogName -Source $eventSource -EntryType "Information" -EventId 0 -Message "Script Started."
     }
 
     catch [System.Security.SecurityException] {
          Write-Error "Error:  Run as elevated user.  Unable to write or read to event logs."
     }
}


# Get events
$scheduledEvents = GetScheduledEvents $scheduledEventURI

# Handle events however is best for your service
HandleScheduledEvents $scheduledEvents

# Approve events when ready (optional)
foreach($event in $scheduledEvents.Events)
{
    Write-Host "Current Event: `n" $event
    $entry = Read-Host "`nApprove event? Y/N"
    if($entry -eq "Y" -or $entry -eq "y")
    {
        ApproveScheduledEvent $event.EventId $scheduledEvents.DocumentIncarnation $scheduledEventURI 
    }
}