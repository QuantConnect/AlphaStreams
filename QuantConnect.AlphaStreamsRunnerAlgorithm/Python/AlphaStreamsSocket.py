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

from QuantConnect import *
from QuantConnect.Data.Custom import *
from AlphaStream.Models import Insight as AlphaStreamInsight

import json
from datetime import datetime
import sys


class AlphaStreamsSocket:
    '''
        Class to create and run threads for each Alpha being subscribed to. It creates threads,
        opens connections to the streaming Insights, and passes them on to the Alpha Model
        for each Alpha ID.
    '''

    def __init__(self, algorithm, client, streamClientInformation, alphaIds):
        '''
            Args:
                algorithm: QC Algorithm allows for logging and access to algorithm class
                client: Alpha Stream Client instance
                streamClientInformation: dictionary holding credentials necessary to establish the connection
        '''
        self.algorithm = algorithm
        self.error = False
        # Added null data source to ensure Update() method fires every second
        self.algorithm.AddData(NullData, 'NullData', Resolution.Second)

        for alphaId in alphaIds:
            try:
                client.Subscribe(alphaId)
            except:
                error = sys.exc_info()[1].args[0]
                msg = "This token is not authorized to license alphas beyond"
                if msg in error:
                    self.algorithm.OnEndOfAlgorithm()
                    raise Exception(f'{error[48:]}')
                else:
                    self.algorithm.Log(f'{error[-18:]} to {alphaId}')
                    self.error = True
            if not self.error:
                self.algorithm.Log(f'Subscribed to {alphaId}')
            else:
                self.error = False


        self.algorithm.Log(f'{datetime.now()} :: Creating RMQ factory')

        # Setting factory properties
        factory = ConnectionFactory()
        factory.HostName = streamClientInformation.get('HostName', None)
        factory.Port = streamClientInformation.get('Port', None)
        factory.UserName = streamClientInformation.get('UserName', None)
        factory.Password = streamClientInformation.get('Password', None)
        factory.VirtualHost = streamClientInformation.get('VirtualHost', None)
        factory.AutomaticRecoveryEnabled = True
        factory.RequestedConnectionTimeout = 5000

        connection = factory.CreateConnection()
        connection.ConnectionBlocked += self.OnConnectionBlocked
        connection.ConnectionShutdown += self.OnConnectionShutdown
        connection.ConnectionUnblocked += self.OnConnectionUnblocked
        connection.CallbackException += self.OnCallbackException

        # Open channel
        self.algorithm.Log(f'{datetime.now()} :: Opening RMQ channel')
        channel = connection.CreateModel()

        # Create consumer to receive messages
        self.algorithm.Log(f'{datetime.now()} :: Creating RMQ consumer')
        consumer = EventingBasicConsumer(channel)
        consumer.Received += self.ConsumerOnReceived


        dict1 = Dictionary[String, Object]()
        dict1["x-message-ttl"] = 60000

        self.algorithm.Log(f'{datetime.now()} :: Creating RMQ Queue')
        channel.QueueDeclare("AlphaStreamsRunner", False, False, True, dict1)
        channel.QueueBind("AlphaStreamsRunner", streamClientInformation.get("ExchangeName", None), f'*', dict1)
        channel.BasicConsume("AlphaStreamsRunner", True, "", False, False, dict1, consumer)
        self.algorithm.Log(f'{datetime.now()} :: RMQ connection established')

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
            self.algorithm.Log(f'{datetime.now()} :: Routing Key: {e.get_RoutingKey()} :: Exchange: {e.get_Exchange()} :: Consumer tag: {e.get_ConsumerTag()} :: Delivery tag: {e.get_DeliveryTag()}')
            messageType = packet.get("eType", None)
            alphaId = packet.get("alpha-id", None)
            model = self.algorithm.alphaModels.get(alphaId, None)

            if model is None:
                # raise Exception (f'Message received from different Alpha: {alphaId}. Check Queue bindings, shutting down algorithm.')
                return

            if messageType == "AlphaResult":
                insights = packet.get("insights", [])
                for insight in insights:
                    self.algorithm.Log(f'{self.algorithm.Time} :: {alphaId} received Insight. Converting to framework Insight')
                    asi = AlphaStreamInsight(insight)
                    model.Listener(model.AlphaInsightToFrameworkInsight(asi))  # Send streamed Insights back into Alpha model

            elif messageType == "AlphaHeartbeat":
                self.algorithm.Log(f'Model: {model.Id}')
                algorithmId = packet.get("algorithm-id", None)
                machineTime = packet.get("machine-time", None)
                self.algorithm.Log(f'Heartbeat :: alphaId: {model.Id} -- algo ID: {algorithmId} :: {machineTime}\n')
            else:
                raise Exception(f"Invalid type: {messageType}")

        except Exception as err:
            self.algorithm.Log(f"Failed parsing deliver event: {err}")
            # self.algorithm.Quit()
