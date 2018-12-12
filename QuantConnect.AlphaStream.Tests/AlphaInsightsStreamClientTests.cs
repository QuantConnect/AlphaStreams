using System;
using System.Threading;
using Newtonsoft.Json;
using NUnit.Framework;
using QuantConnect.AlphaStream.Requests;

namespace QuantConnect.AlphaStream.Tests
{
    [TestFixture, Ignore("These tests require a subscription a specific QuantConnect Alpha Stream.")]
    public class AlphaInsightsStreamClientTests
    {
        // set credentials for connecting to your alpha streams exchange
        private const string HostName = "35.231.13.1";
        private const string UserName = "demo-api";
        private const string Password = "demo";
        private const string VirtualHost = "demo-client";
        private const string ExchangeName = "QCAlphaExchange_Demo-Client";

        [Test]
        public void StreamsInsightsTest()
        {
            var info = new AlphaInsightsStreamCredentials(
                HostName,
                5672,
                UserName,
                Password,
                ExchangeName,
                VirtualHost
                );

            var client = new AlphaInsightsStreamClient(info);
            client.Connect();

            client.InsightReceived += (sender, args) =>
            {
                Console.WriteLine(JsonConvert.SerializeObject(args, Formatting.Indented));
            };

            client.HeartbeatReceived += (sender, args) =>
            {
                Console.WriteLine(JsonConvert.SerializeObject(args, Formatting.Indented));
            };

            client.AddAlphaStream(new AddInsightsStreamRequest { AlphaId = "392a40ccab3740287a1c30bc6" });

            Thread.Sleep(60000);
            client.Dispose();
        }
    }
}