using System;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Defines the required connection information for connection to alpha streams streaming server
    /// </summary>
    public class AlphaStreamConnectionInformation
    {
        public string HostName { get; }
        public int Port { get; }
        public string Username { get; }
        public string Password { get; }
        public string ExchangeName { get; }
        public string VirtualHost { get; }
        public bool AutomaticRecoveryEnabled { get; }
        public int RequestedConnectionTimeout { get; }
        public string ConsumerTag { get; }

        public AlphaStreamConnectionInformation(string hostName,
            int port,
            string username,
            string password,
            string exchangeName,
            string virtualHost = "/",
            bool automaticRecoveryEnabled = true,
            int requestedConnectionTimeout = 5000,
            string consumerTag = null
            )
        {
            HostName = hostName;
            Port = port;
            Username = username;
            Password = password;
            ExchangeName = exchangeName;
            VirtualHost = virtualHost;
            AutomaticRecoveryEnabled = automaticRecoveryEnabled;
            RequestedConnectionTimeout = requestedConnectionTimeout;

            // uniquely identify this consumer
            ConsumerTag = consumerTag ?? Guid.NewGuid().ToString("N");
        }
    }
}