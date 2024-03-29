'''
Created on Oct 17, 2012

A basic implementation of the RMAS esb specification that uses mongodb as a backend

@author: jasonmarshall
'''

import logging
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import Unicode, Boolean
from spyne.model.complex import Iterable
from spyne.util.simple import wsgi_soap_application
from wsgiref.simple_server import make_server
from datetime import datetime
import dateutil.parser
from pymongo import Connection
from rmasservicebus.EventValidator import validate_rmas_event
from pymongo.errors import PyMongoError

database = None
message_collection = None

class RMASService(ServiceBase):

    @srpc(Unicode, _returns=Boolean)
    def pushEvent(event):
        '''
        Push an event onto the RMAS bus queue
        @param message a valid RMAS event
        @return whether or not the message was succesfully pushed (most likely reason for False is invalid maessage)
        '''
        logging.info('attempting to push event to the queue: %s' % event)
        
        if validate_rmas_event(event):
            try:
                message = {'event':event,
                           'received':datetime.now()}
                message_collection.insert(message)
                logging.info("shoved message in the queue: %s" % event)
                return True
            except Exception:
                logging.error("Failed to add the message to the queue!")
                pass
        else:
            logging.error('Not a valid message: %s' % event)
        
        return False
    
    @srpc(Unicode, _returns=Iterable(Unicode))
    def getEvents(timestamp):
        '''
            Returns the RMAS events that have been received after the given timestamp
            @param timestamp the ISO-8601 timestamp, messages after this time will be delivered
            @return a list of RMAS events.
        '''
        
        logging.info('call to getEvents with timestamp: %s' % timestamp)
        
        try:
            datetime = dateutil.parser.parse(timestamp)
        except ValueError as e:
            logging.error('There was a Value Error parsing the timestamp %s: e' % (timestamp, e))

        
        #query the messages collection based on the datetime
        try:
            messages = [message['event'] for message in message_collection.find({"received": {"$gt": datetime}})]
            return messages
        except PyMongoError as e:
            logging.error('An error occurred whilst querying the database: %s'% e)

        return []
if __name__=='__main__':
    
    connection = Connection()
    database = connection.rmas_messages
    message_collection = database.message_collection
    
    
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.INFO)

    logging.info("listening to http://127.0.0.1:7789")
    logging.info("wsdl is at: http://localhost:7789/?wsdl")

    wsgi_app = wsgi_soap_application([RMASService], 'spyne.examples.hello.soap')
    server = make_server('127.0.0.1', 7789, wsgi_app)
    server.serve_forever()
    
    
    
    
    

