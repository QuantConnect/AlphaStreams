
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using Newtonsoft.Json.Linq;
using QuantConnect.AlphaStream.Models;
using QuantConnect.AlphaStream.Models.Orders;
using QuantConnect.AlphaStream.Requests;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using RabbitMQ.Client.Framing.Impl;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Client used to stream live alpha insights, orders and order events.
    /// </summary>
    public class AlphaStreamEventClient : IAlphaStreamClient
    {
        private IModel channel;
        private IConnection connection;
        private readonly AlphaStreamCredentials credentials;
        private readonly Dictionary<string, EventingBasicConsumer> consumersByAlphaId;

        /// <summary>
        /// Event fired for each insight received
        /// </summary>
        public event EventHandler<InsightReceivedEventArgs> InsightReceived;

        /// <summary>
        /// Event fired when a heartbeat is received
        /// </summary>
        public event EventHandler<HeartbeatReceivedEventArgs> HeartbeatReceived;

        /// <summary>
        /// Event fired when a new Order or an update is received
        /// </summary>
        public event EventHandler<OrderReceivedEventArgs> OrderReceived;

        /// <summary>
        /// Initializes a new instance of the <see cref="AlphaStreamEventClient"/> class
        /// </summary>
        /// <param name="credentials">The exchange information where the alphas data is disseminated from</param>
        public AlphaStreamEventClient(AlphaStreamCredentials credentials)
        {
            this.credentials = credentials;
            consumersByAlphaId = new Dictionary<string, EventingBasicConsumer>();
        }

        /// <summary>
        /// Adds a new alpha to be streamed
        /// </summary>
        public bool AddAlphaStream(AddAlphaStreamRequest request)
        {
            if (channel == null)
            {
                Connect();
            }

            if (consumersByAlphaId.ContainsKey(request.AlphaId))
            {
                Error($"Already bound to alpha stream: {request.AlphaId}");
                return false;
            }

            // define our consumer
            var consumer = new EventingBasicConsumer(channel);
            consumer.Received += ConsumerOnReceived;
            consumer.Registered += ConsumerOnRegistered;
            consumer.Shutdown += ConsumerOnShutdown;
            consumer.Unregistered += ConsumerOnUnregistered;

            // declare and bind to queue (queue declaration is idempotent)
            channel.QueueDeclare(request.AlphaId, false, false,
                arguments: new Dictionary<string, object> { { "x-message-ttl", 60000 } });
            channel.QueueBind(request.AlphaId, credentials.ExchangeName, request.AlphaId);
            channel.BasicConsume(consumer, request.AlphaId, true);

            consumersByAlphaId.Add(request.AlphaId, consumer);

            Info($"Begin streaming insights for alpha stream: {request.AlphaId}");
            return true;
        }

        /// <summary>
        /// Removes an alpha being streamed
        /// </summary>
        public bool RemoveAlphaStream(RemoveAlphaStreamRequest request)
        {
            if (channel == null)
            {
                Connect();
            }

            EventingBasicConsumer consumer;
            if (!consumersByAlphaId.TryGetValue(request.AlphaId, out consumer))
            {
                Error($"Bind to alpha stream first by calling AddInsightsStream({request.AlphaId})");
                return false;
            }

            // unbind from the queue and unregister our event handler
            channel.QueueUnbind(request.AlphaId, credentials.ExchangeName, request.AlphaId);
            consumer.Received -= ConsumerOnReceived;
            consumer.Registered -= ConsumerOnRegistered;
            consumer.Shutdown -= ConsumerOnShutdown;
            consumer.Unregistered -= ConsumerOnUnregistered;

            Info($"End streaming insights for alpha stream: {request.AlphaId}");
            return true;
        }

        /// <summary>
        /// Connects the alpha stream client
        /// </summary>
        public void Connect()
        {
            if (channel != null)
            {
                Error("Already connected");
                return;
            }

            var factory = new ConnectionFactory
            {
                HostName = credentials.HostName,
                Port = credentials.Port,
                UserName = credentials.Username,
                Password = credentials.Password,
                VirtualHost = credentials.VirtualHost,
                AutomaticRecoveryEnabled = credentials.AutomaticRecoveryEnabled,
                RequestedConnectionTimeout = credentials.RequestedConnectionTimeout
            };

            Info($"Connecting to exchange '{credentials.ExchangeName}' at {factory.HostName}:{factory.Port}...");

            connection = factory.CreateConnection();
            connection.ConnectionBlocked += OnConnectionBlocked;
            connection.ConnectionShutdown += OnConnectionShutdown;
            connection.ConnectionUnblocked += OnConnectionUnblocked;
            connection.CallbackException += OnCallbackException;

            // add event handler for auto recovering events
            var autorecovering = connection as AutorecoveringConnection;
            if (autorecovering != null)
            {
                autorecovering.RecoverySucceeded += OnRecoverySucceeded;
                autorecovering.QueueNameChangeAfterRecovery += OnQueueNameChangeAfterRecovery;
                autorecovering.ConsumerTagChangeAfterRecovery += OnConsumerTagChangeAfterRecovery;
            }

            channel = connection.CreateModel();

            Info($"Connected to exchange '{credentials.ExchangeName}");
        }

        /// <summary>
        /// Disposes of the alpha stream connection
        /// </summary>
        public void Dispose()
        {
            try
            {
                channel?.Dispose();
                channel = null;
            }
            catch (Exception exception)
            {
                Error($"Exception disposing of channel {exception.Message}");
            }

            try
            {
                connection?.Dispose();
            }
            catch (Exception exception)
            {
                Error($"Exception disposing of connection {exception.Message}");
            }
        }

        protected virtual void OnInsightReceived(InsightReceivedEventArgs e)
        {
            InsightReceived?.Invoke(this, e);
        }

        protected virtual void OnOrderReceived(OrderReceivedEventArgs e)
        {
            OrderReceived?.Invoke(this, e);
        }

        protected virtual void OnAlphaHeartbeatReceived(HeartbeatReceivedEventArgs e)
        {
            HeartbeatReceived?.Invoke(this, e);
        }

        #region Consumer Events

        protected void ConsumerOnUnregistered(object sender, ConsumerEventArgs e)
        {
            Info($"Consumer Unregistered: {e.ConsumerTag}");
        }

        protected void ConsumerOnShutdown(object sender, ShutdownEventArgs e)
        {
            Error($"Consumer Shutdown: Code: {e.ReplyCode}. {e.ReplyText} Cause: {e.Cause}");
        }

        protected void ConsumerOnRegistered(object sender, ConsumerEventArgs e)
        {
            Info($"Consumer Registered: {e.ConsumerTag}");
        }

        protected void ConsumerOnReceived(object sender, BasicDeliverEventArgs e)
        {
            try
            {
                var body = Encoding.UTF8.GetString(e.Body);
                var packet = JObject.Parse(body);

                var type = packet["eType"]?.Value<string>();
                var alphaId = packet["alpha-id"]?.Value<string>() ?? packet["AlphaId"].Value<string>();

                if (type.Equals("AlphaResult"))
                {
                    var insights = packet["insights"]?.ToObject<List<Insight>>();
                    if (insights != null)
                    {
                        foreach (var insight in insights)
                        {
                            OnInsightReceived(new InsightReceivedEventArgs(alphaId, insight));
                        }
                    }
                    var orders = packet["orders"]?.ToObject<List<Order>>();
                    if (orders != null)
                    {
                        var orderEvents = packet["order-events"]?.ToObject<List<OrderEvent>>();
                        foreach (var order in orders)
                        {
                            order.Source = "live trading";
                            if (orderEvents != null)
                            {
                                order.OrderEvents =
                                    orderEvents.Where(orderEvent => orderEvent.Id.Contains(order.Id)).ToList();
                            }
                            else
                            {
                                // this won't happen, orders and associated order events are sent together
                                Error($"No OrderEvents were provided for order {order.Id}");
                            }
                            OnOrderReceived(new OrderReceivedEventArgs(alphaId, order));
                        }
                    }
                }
                else if (type.Equals("AlphaHeartbeat"))
                {
                    var algorithmId = packet["algorithm-id"]?.Value<string>();
                    var machineTime = packet["machine-time"]?.Value<DateTime>();
                    OnAlphaHeartbeatReceived(new HeartbeatReceivedEventArgs(alphaId, algorithmId, machineTime));
                }
                else
                {
                    throw new Exception($"Invalid type: {type}");
                }
            }
            catch (Exception err)
            {
                Info("Failed parsing deliver event: " + err);
            }
        }

        #endregion

        #region Connection Events

        protected void OnCallbackException(object sender, CallbackExceptionEventArgs e)
        {
            var detail = string.Join(" | ", e.Detail.Select(kvp => $"{kvp.Key}:{kvp.Value}"));
            Error("Callback Exception: " + e.Exception);
            Error("Callback Detail: " + detail);
        }

        protected void OnConnectionUnblocked(object sender, EventArgs e)
        {
            Info("Connection Unblocked.");
        }

        protected void OnConnectionShutdown(object sender, ShutdownEventArgs e)
        {
            Error($"Connection Shutdown: Code: {e.ReplyCode}. {e.ReplyText} Cause: {e.Cause}");
        }

        protected void OnConnectionBlocked(object sender, ConnectionBlockedEventArgs e)
        {
            Error($"Connection Blocked: {e.Reason}");
        }

        protected void OnRecoverySucceeded(object sender, EventArgs e)
        {
            Info("Recovery Succeeded.");
        }

        protected void OnQueueNameChangeAfterRecovery(object sender, QueueNameChangedAfterRecoveryEventArgs e)
        {
            Info($"Queue Name Changed: Before: {e.NameBefore} After: {e.NameAfter}");
        }

        protected void OnConsumerTagChangeAfterRecovery(object sender, ConsumerTagChangedAfterRecoveryEventArgs e)
        {
            Info($"Consumer Tag Changed: Before: {e.TagBefore} After: {e.TagAfter}");
        }

        #endregion

        private void Info(string message)
        {
            Trace.TraceInformation($"{credentials.ExchangeName}|{credentials.ConsumerTag}: {message}");
        }

        private void Error(string message)
        {
            Trace.TraceError($"{credentials.ExchangeName}|{credentials.ConsumerTag}: {message}");
        }
    }
}
