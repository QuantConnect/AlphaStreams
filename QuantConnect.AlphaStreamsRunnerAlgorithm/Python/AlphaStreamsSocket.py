from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Common")
AddReference("RabbitMQ.Client")

from RabbitMQ.Client import *
from RabbitMQ.Client.Events import *

from System import *
from System import String, Object
from System.Text import *
from System.Collections.Generic import Dictionary
from AlphaStream.Models import Insight as AlphaStreamInsight

import json
import threading
from NullData import *


class AlphaStreamsSocket:
    '''
        Class to create and run threads for each Alpha being subscribed to. It creates threads,
        opens connections to the streaming Insights, and passes them on to the Alpha Model
        for each Alpha ID.
    '''

    def __init__(self, algorithm):
        '''
            Args:
                algorithm: QC Algorithm allows for logging and access to algorithm class
        '''
        self.algorithm = algorithm
        self.channel = self.factory = self.connection = self.consumer = None
        self.thread_return = {}

        # Added null data source to ensure Update() method fires every second
        algorithm.AddData(NullData, 'NullDataSource', Resolution.Second)

    def AddAlphaStream(self, alphaId, client, streamClientInformation):
        ''' Creates and opens a connection to an Alpha, and consumes the messages
            being sent.

            Args:
                alphaId: ID of the Alpha being subscribed to
                client: Alpha Stream Client instance
                streamClientInformation: dictionary holding credentials necessary to establish the connection
        '''
        try:
            client.Subscribe(alphaId)
            self.algorithm.Log(f'Subscribing to {alphaId}')
        except:
            client.Unsubscribe(alphaId)
            client.Subscribe(alphaId)

        # Setting factory properties
        factory = ConnectionFactory()
        factory.HostName = streamClientInformation.get('HostName', None)
        factory.Port = streamClientInformation.get('Port', None)
        factory.UserName = streamClientInformation.get('UserName', None)
        factory.Password = streamClientInformation.get('Password', None)
        factory.VirtualHost = streamClientInformation.get('VirtualHost', None)
        factory.AutomaticRecoveryEnabled = True
        factory.RequestedConnectionTimeout = 5000

        # Opening connection to AMQP broker
        connection = factory.CreateConnection()
        connection.ConnectionBlocked += self.OnConnectionBlocked
        connection.ConnectionShutdown += self.OnConnectionShutdown
        connection.ConnectionUnblocked += self.OnConnectionUnblocked
        connection.CallbackException += self.OnCallbackException

        # Open channel
        channel = connection.CreateModel()

        # Create consumer to receive messages
        consumer = EventingBasicConsumer(channel)
        consumer.Received += self.ConsumerOnReceived

        dict1 = Dictionary[String, Object]()
        dict1["x-message-ttl"] = 60000

        channel.QueueDeclare(alphaId, False, False, True, dict1)
        channel.QueueBind(alphaId, streamClientInformation.get("ExchangeName", None), alphaId, dict1)
        channel.BasicConsume(alphaId, True, "", False, False, dict1, consumer)
        self.algorithm.Log(f'Connection established')

    def OnConnectionBlocked(self, sender, args):
        self.algorithm.Log(f"RMQHelper.OnConnectionBlocked(): Connection is blocked: {args.Reason}")

    def OnConnectionShutdown(self, sender, args):
        self.algorithm.Log(f"RMQHelper.OnConnectionShutdown(): Connection is shutdown: {args.Reason}")

    def OnConnectionUnblocked(self, sender, args):
        self.algorithm.Log(f"RMQHelper.OnConnectionUnblocked(): Connection is unblocked: {args.Reason}")

    def OnCallbackException(self, sender, args):
        self.algorithm.Log(f"RMQHelper.OnCallbackException(): Callback exception: {args.Reason}")

    def ConsumerOnReceived(self, sender, e):
        ''' Consumes and processes the messages received via the channel '''
        try:
            stringDictionary = Encoding.UTF8.GetString(e.Body)
            packet = json.loads(stringDictionary)
            messageType = packet.get("eType", None)
            alphaId = packet.get("alpha-id", None)
            model = self.algorithm.alphaModels.get(alphaId, None)

            if model is None:
                # raise Exception (f'Message received from different Alpha: {alphaId}. Check Queue bindings, shutting down algorithm.')
                return

            if messageType == "AlphaResult":
                insights = packet.get("insights", [])
                for insight in insights:
                    asi = AlphaStreamInsight(insight)
                    model.Listener(
                        model.AlphaInsightToFrameworkInsight(asi))  # Send streamed Insights back into Alpha model

            elif messageType == "AlphaHeartbeat":
                algorithmId = packet.get("algorithm-id", None)
                machineTime = packet.get("machine-time", None)
                self.algorithm.Log(f'Heartbeat :: algo ID: {algorithmId} :: {machineTime}')
            else:
                raise Exception(f"Invalid type: {messageType}")

        except Exception as err:
            self.algorithm.Log(f"Failed parsing deliver event: {err}")
            # self.algorithm.Quit()

    # Create thread for each Alpha ID to stream Insights independently
    def Stream(self, alphaIds, client, streamClientInformation):
        ''' Stream creates threads and executes the target functions in each. This keeps the channels open
            to receive Insights so long as the connection remains valid. If there is an error, it throws and closes all threads.

            Args:
                alphaId: ID of the Alpha being subscribed to
                client: Alpha Stream Client instance
                streamClientInformation: dictionary holding credentials necessary to establish the connection
        '''

        threads = []
        try:
            for id in alphaIds:
                self.algorithm.Log(f'Creating thread for alpha {id}')
                thread = threading.Thread(target=self.AddAlphaStream, args=(id, client, streamClientInformation,))
                self.algorithm.Log(f'Thread created. Starting thread')
                thread.start()
                threads.append(thread)

        except Exception as err:
            self.algorithm.Log(f'Exception thrown in threading. Closing threads: {err}')
            for t in threads:
                t.join()
