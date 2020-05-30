import win32evtlog, win32event


ADIP = '10.0.0.x'       # IP address of your domain controller
ADusername = ''         # Name of the account you will use to connect to AD
ADdomain = ''           # Domain (domain.local / domain.com)
ADuserpass = ''         # Password for the above user

eventIDs = [5379]       # List of EventIDs to watch for
eventlog = 'security'   # Which log to watch (security, application, setup, system, etc.)

evtSessionCredentials = (ADIP, ADusername, ADdomain, ADuserpass, win32evtlog.EvtRpcLoginAuthDefault)
evtSession = win32evtlog.EvtOpenSession(evtSessionCredentials, win32evtlog.EvtRpcLogin, 0, 0)

XPathQuery = "*[System[({})]".format(' or '.join("EventID="+str(x) for x in eventIDs))  # The XPath-styled query to tell the domain controller which events to return

#evt1: int specifying why the function was called | evt2: context object (5th parameter in EvtSubscribe) | evt3: event content
def eventTriggered(evt1, evt2, evt3):
    print("Triggered")
    print(evt1)
    print(evt2)
    print(win32evtlog.EvtRender(evt3, win32evtlog.EvtRenderEventXml))
    win32event.PulseEvent(evtHandle)

evtHandle = win32event.CreateEvent(None, 0, 0, None)
x = win32evtlog.EvtSubscribe(eventlog, win32evtlog.EvtSubscribeToFutureEvents, None, eventTriggered, None, XPathQuery, None, None)
while True:
    if win32event.WaitForSingleObject(evtHandle, 600000) == win32event.WAIT_OBJECT_0:   # Not really necessary to have this or PulseEvent. Probably better to do everything in eventTriggered.
        # print(win32evtlog.EvtRender(x, win32evtlog.EvtRenderEventXml))
        pass
    else:
        print('timeout')
