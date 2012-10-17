A basic implementation of the RMAS esb specification that uses mongodb as a backend

NB. You will need to have mongodb instlled and running for this to work

example usage:
'''
>>> from suds.client import Client
>>> c = Client('http://localhost:7789/?wsdl', cache=None)
>>> print c

Suds ( https://fedorahosted.org/suds/ )  version: 0.4 GA  build: R699-20100913

Service ( RMASService ) tns="spyne.examples.hello.soap"
   Prefixes (1)
      ns0 = "spyne.examples.hello.soap"
   Ports (1):
      (Application)
         Methods (2):
            getEvents(xs:string timestamp, )
            pushEvent(xs:string event, )
         Types (5):
            getEvents
            getEventsResponse
            pushEvent
            pushEventResponse
            stringArray

>>> from datetime import datetime
>>> before = datetime.now()
>>> c.service.pushEvent('a very special message')
True
>>> c.service.pushEvent('another very special message')
True
>>> c.service.getEvents(before.isoformat())
(stringArray){
   string[] = 
      "a very special message",
      "another very special message",
 }

>>> now = datetime.now()
>>> c.service.getEvents(now.isoformat())
'''
 
