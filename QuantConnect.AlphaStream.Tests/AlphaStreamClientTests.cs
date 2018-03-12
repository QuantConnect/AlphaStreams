using System;
using System.Threading;
using Newtonsoft.Json;
using NUnit.Framework;
using QuantConnect.AlphaStream.Requests;

namespace QuantConnect.AlphaStream.Tests
{
    [TestFixture, Ignore("These tests require a subscription a specific QuantConnect Alpha Stream.")]
    public class AlphaStreamClientTests
    {
        // set credentials for connecting to your alpha streams exchange
        private const string HostName = null;
        private const string UserName = null;
        private const string Password = null;
        private const string ExchangeName = null;

        [Test]
        public void StreamsInsightsTest()
        {
            var info = new AlphaStreamConnectionInformation(
                HostName,
                5672,
                UserName,
                Password,
                ExchangeName
                );

            var client = new AlphaInsightsStreamClient(info);
            client.Connect();

            client.InsightReceived += (sender, args) =>
            {
                Console.WriteLine(JsonConvert.SerializeObject(args, Formatting.Indented));
            };

            client.AddAlphaStream(new AddInsightsStreamRequest
            {
                AlphaId = "623b06b231eb1cc1aa3643a46"
            });

            Thread.Sleep(60000);
            client.Dispose();
        }
    }
}