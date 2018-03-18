import json
import time
import pika
import queue

from Models.Insight import Insight
from Models.InsightPackage import InsightPackage


class AlphaInsightsStreamClient(object):
    """Alpha Streams Streaming Client """

    def __init__(self, user, password, ipaddress, virtualhost, exchange):
        self.__url = 'amqp://{}:{}@{}:5672/{}'.format(user, password, ipaddress, virtualhost)
        self.__exchange = exchange
        self.__workQueue = queue.Queue()
        
        # Create connection:
        credentials = pika.PlainCredentials(user, password)
        parameters = pika.ConnectionParameters(ipaddress, 5672, virtualhost, credentials)
        
        # Declare queue and bind to exchange:
        self.__connection = pika.BlockingConnection( parameters )
        self.__channel = self.__connection.channel()
        

    def StreamSynchronously(self, alphaId, timeout=10):
        """ Stream a specific alpha id to a supplied callback method for timeout seconds. """
        result = self.__channel.queue_declare(queue=alphaId, durable=False, exclusive=False, auto_delete=True)
        queue = self.__channel.queue_bind(exchange=self.__exchange, queue=alphaId, routing_key=alphaId)
        end = time.time() + timeout
        
        # Stream out queue for period.
        while time.time() < end:
            method, properties, body = self.__channel.basic_get(alphaId, no_ack=True)
            if method:
                # Process the package container
                decoded = json.loads(body)
                insightPackage = InsightPackage(decoded)
                
                # Yield only the insights themselves.
                for i in insightPackage.Insights:
                    yield i
            else:
                time.sleep(0.01)
                
        #Tidy up
        self.__channel.queue_unbind(queue=alphaId, exchange=self.__exchange, routing_key=alphaId)
        self.__channel.queue_delete(queue=alphaId, if_unused=True)
        self.__channel.close()
            