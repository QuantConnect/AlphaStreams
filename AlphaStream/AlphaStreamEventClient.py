import pika
from json import loads
from time import sleep, time

from .Models import HeartbeatPackage
from .Models import AlphaResultPackage


class AlphaStreamEventClient(object):
    """Alpha Streams Streaming Client """

    def __init__(self, user, password, ipaddress, virtualhost, exchange):
        self.__exchange = exchange

        # Create connection, pass Rabbit MQ credentials
        credentials = pika.PlainCredentials(user, password)
        parameters = pika.ConnectionParameters(ipaddress, 5672, virtualhost, credentials)

        # Declare queue and bind to exchange:
        self.__connection = pika.BlockingConnection(parameters)
        self.__channel = self.__connection.channel()

    def StreamSynchronously(self, alphaId, timeout=10):
        """ Stream a specific alpha id to a supplied callback method for timeout seconds. """
        result = self.__channel.queue_declare(queue=alphaId, durable=False, exclusive=False, auto_delete=True,
                                              arguments={'x-message-ttl': 60000})
        queue = self.__channel.queue_bind(exchange=self.__exchange, queue=alphaId, routing_key=alphaId)
        end = time() + timeout

        # Stream out queue for period.
        while time() < end:
            method, properties, body = self.__channel.basic_get(alphaId, auto_ack=True)
            if method:
                # Process the package container
                decoded = loads(body)
                if decoded['alpha-id'] != alphaId:
                    continue

                etype = decoded['eType']
                # Alpha results are either Insights or Orders
                if etype == 'AlphaResult':
                    package = AlphaResultPackage(decoded)

                    # Yield the insights
                    for i in package.Insights:
                        yield i

                    # Yield the orders
                    for order in package.Orders:
                        yield order

                # Heartbeat is emitted once per minute to show connection is open
                elif etype == 'AlphaHeartbeat':
                    yield HeartbeatPackage(decoded)

                else:
                    raise Exception(f'Invalid type: {etype}')
            else:
                sleep(0.01)

        # Tidy up
        self.__channel.queue_unbind(queue=alphaId, exchange=self.__exchange, routing_key=alphaId)
        self.__channel.queue_delete(queue=alphaId, if_unused=True)
        self.__channel.close()