using System;
using System.ComponentModel;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Defines the required connection information for connection to alpha streams streaming server
    /// </summary>
    public class AlphaInsightsStreamCredentials
    {
        [JsonProperty("rabbitmq-address")]
        public string HostName { get; set; }

        [JsonProperty("rabbitmq-port")]
        public int Port { get; set; } = 5672;

        [JsonProperty("rabbitmq-user")]
        public string Username { get; set; }

        [JsonProperty("rabbitmq-password")]
        public string Password { get; set; }

        [JsonProperty("rabbitmq-exchange")]
        public string ExchangeName { get; set; }

        [JsonProperty("rabbitmq-virtualhost")]
        public string VirtualHost { get; set; } = "/";

        [JsonProperty("rabbitmq-auto-recovery-enabled"), DefaultValue(true)]
        public bool AutomaticRecoveryEnabled { get; set; } = true;

        [JsonProperty("rabbitmq-timeout")]
        public int RequestedConnectionTimeout { get; set; } = 5000;

        [JsonProperty("rabbitmq-consumer-tag"), DefaultValue(null)]
        public string ConsumerTag { get; set; }

        public AlphaInsightsStreamCredentials()
        {
        }

        public AlphaInsightsStreamCredentials(string hostName,
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

        public static AlphaInsightsStreamCredentials FromConfiguration()
        {
            if (!File.Exists("config.json"))
            {
                throw new FileNotFoundException("Please specify 'alpha-credentials-path' in 'config.json'");
            }

            var config = JObject.Parse(File.ReadAllText("config.json"));
            var credentialsPath = config["alpha-credentials-path"];
            if (credentialsPath == null)
            {
                throw new Exception("Please specify 'alpha-credentials-path' in 'config.json'");
            }

            return FromFile(credentialsPath.Value<string>());
        }

        public static AlphaInsightsStreamCredentials FromFile(string path)
        {
            if (!File.Exists(path))
            {
                throw new FileNotFoundException($"AlphaInsightsStreamCredentials file not found: {path}");
            }

            return JsonConvert.DeserializeObject<AlphaInsightsStreamCredentials>(File.ReadAllText(path));
        }
    }
}