using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using Newtonsoft.Json.Linq;
using QuantConnect.AlphaStream.Models;
using QuantConnect.AlphaStream.Requests;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using RabbitMQ.Client.Framing.Impl;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Client used to stream live alpha insights.
    /// </summary>
    public class AlphaInsightsStreamClient : IAlphaInsightsStreamClient
    {
        private IModel channel;
        private IConnection connection;
        private readonly AlphaStreamConnectionInformation connectionInformation;
        private readonly Dictionary<string, EventingBasicConsumer> consumersByAlphaId;

        public event EventHandler<InsightReceivedEventArgs> InsightReceived;

        /// <summary>
        /// Initializes a new instance of the <see cref="AlphaInsightsStreamClient"/> class
        /// </summary>
        /// <param name="connectionInformation">The exchange information where the insights are disseminated from</param>
        public AlphaInsightsStreamClient(AlphaStreamConnectionInformation connectionInformation)
        {
            this.connectionInformation = connectionInformation;
            consumersByAlphaId = new Dictionary<string, EventingBasicConsumer>();
        }

        public void Connect()
        {
            var factory = new ConnectionFactory
            {
                HostName = connectionInformation.HostName,
                Port = connectionInformation.Port,
                UserName = connectionInformation.Username,
                Password = connectionInformation.Password,
                VirtualHost = connectionInformation.VirtualHost,
                AutomaticRecoveryEnabled = connectionInformation.AutomaticRecoveryEnabled,
                RequestedConnectionTimeout = connectionInformation.RequestedConnectionTimeout
            };

            Info("Connecting... ");

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
        }

        public bool AddAlphaStream(AddInsightsStreamRequest request)
        {
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
            channel.QueueDeclare(request.AlphaId, false, false);
            channel.QueueBind(request.AlphaId, connectionInformation.ExchangeName, request.AlphaId);
            channel.BasicConsume(consumer, request.AlphaId, true);

            consumersByAlphaId.Add(request.AlphaId, consumer);

            Info($"Begin streaming insights for alpha stream: {request.AlphaId}");
            return true;
        }

        public bool RemoveAlphaStream(RemoveInsightsStreamRequest request)
        {
            EventingBasicConsumer consumer;
            if (!consumersByAlphaId.TryGetValue(request.AlphaId, out consumer))
            {
                Error($"Bind to alpha stream first by calling AddInsightsStream({request.AlphaId})");
                return false;
            }

            // unbind from the queue and unregister our event handler
            channel.QueueUnbind(request.AlphaId, connectionInformation.ExchangeName, request.AlphaId);
            consumer.Received -= ConsumerOnReceived;
            consumer.Registered -= ConsumerOnRegistered;
            consumer.Shutdown -= ConsumerOnShutdown;
            consumer.Unregistered -= ConsumerOnUnregistered;

            Info($"End streaming insights for alpha stream: {request.AlphaId}");
            return true;
        }

        public void Dispose()
        {
            connection?.Dispose();
        }

        protected virtual void OnInsightReceived(InsightReceivedEventArgs e)
        {
            InsightReceived?.Invoke(this, e);
        }

        #region Consumer Events

        protected void ConsumerOnUnregistered(object sender, ConsumerEventArgs e)
        {
            Info("Consumer Unregistered: " + e.ConsumerTag);
        }

        protected void ConsumerOnShutdown(object sender, ShutdownEventArgs e)
        {
            Error("Consumer Shutdown: Code: {e.ReplyCode}. {e.ReplyText} Cause: {e.Cause}");
        }

        protected void ConsumerOnRegistered(object sender, ConsumerEventArgs e)
        {
            Info("Consumer Registered: {e.ConsumerTag}");
        }

        protected void ConsumerOnReceived(object sender, BasicDeliverEventArgs e)
        {
            try
            {
                var body = Encoding.UTF8.GetString(e.Body);
                var packet = JObject.Parse(body);
                var alphaId = packet["alpha-id"]?.Value<string>() ?? packet["AlphaId"].Value<string>();
                var insights = packet["insights"].ToObject<List<Insight>>();
                foreach (var insight in insights)
                {
                    OnInsightReceived(new InsightReceivedEventArgs(alphaId, insight));
                }
            }
            catch (Exception err)
            {
                Info("Failed parsing insights: " + err);
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
            Error("Connection Shutdown: Code: {e.ReplyCode}. {e.ReplyText} Cause: {e.Cause}");
        }

        protected void OnConnectionBlocked(object sender, ConnectionBlockedEventArgs e)
        {
            Error("Connection Blocked: {e.Reason}");
        }

        protected void OnRecoverySucceeded(object sender, EventArgs e)
        {
            Info("Recovery Succeeded.");
        }

        protected void OnQueueNameChangeAfterRecovery(object sender, QueueNameChangedAfterRecoveryEventArgs e)
        {
            Info("Queue Name Changed: Before: {e.NameBefore} After: {e.NameAfter}");
        }

        protected void OnConsumerTagChangeAfterRecovery(object sender, ConsumerTagChangedAfterRecoveryEventArgs e)
        {
            Info("Consumer Tag Changed: Before: {e.TagBefore} After: {e.TagAfter}");
        }

        #endregion

        private void Info(string message)
        {
            Trace.TraceInformation($"{connectionInformation.ExchangeName}|{connectionInformation.ConsumerTag}: {message}");
        }

        private void Error(string message)
        {
            Trace.TraceError($"{connectionInformation.ExchangeName}|{connectionInformation.ConsumerTag}: {message}");
        }
    }
}