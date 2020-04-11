using System;
using System.Threading;
using NUnit.Framework;
using QuantConnect.AlphaStream.Models;
using QuantConnect.AlphaStream.Requests;

namespace QuantConnect.AlphaStream.Tests
{
    [TestFixture]
    public class AlphaStreamClientTests
    {

        // set credentials for connecting to your alpha streams exchange
        private const string HostName = "35.231.13.1";
        private const string UserName = "demo-api";
        private const string Password = "demo";
        private const string VirtualHost = "demo-client";
        private const string ExchangeName = "QCAlphaExchange_Demo-Client";
        private const string TestAlphaId = "31ac5498164db7341b041a732";

        private AlphaStreamRestClient restClient = new AlphaStreamRestClient(Credentials.Test);

        [Test]
        public void StreamTest()
        {
            /// Set up proper conditions
            try
            {
                var subscribeSetupRequest = new SubscribeRequest { Id = TestAlphaId, Exclusive = false };
                var subscribeSetupResponse = restClient.Execute(subscribeSetupRequest).ConfigureAwait(false);
                var unsubscribeSetupRequest = new UnsubscribeRequest { Id = TestAlphaId };
                var unsubscribeSetupResponse = restClient.Execute(unsubscribeSetupRequest).ConfigureAwait(false);
            }
            catch
            {
                var setupRequest = new UnsubscribeRequest { Id = TestAlphaId };
                var setupResponse = restClient.Execute(setupRequest).ConfigureAwait(false);
            }

            var subscribeRequest = new SubscribeRequest { Id = TestAlphaId, Exclusive = false };
            var subscribeResponse = restClient.Execute(subscribeRequest).ConfigureAwait(false);

            var info = new AlphaStreamCredentials(
                HostName,
                5672,
                UserName,
                Password,
                ExchangeName,
                VirtualHost
                );

            var client = new AlphaStreamEventClient(info);
            client.Connect();

            client.InsightReceived += (sender, args) =>
            {
                Assert.AreEqual(args.Insight.Direction, Direction.Flat);
                Assert.AreEqual(args.Insight.Source, InsightSource.LiveTrading);
                Assert.AreEqual(args.Insight.Period, 86400.0);
                Assert.AreEqual(args.Insight.SymbolId, "BTCUSD XJ");
                Assert.AreEqual(args.Insight.Type, InsightType.Price);
                Assert.AreEqual(args.Insight.SourceModel, "529f1bfe-00d4-4d2b-9787-17532dbeb449");
                Assert.AreEqual(args.Insight.Weight, 0.5);
                Assert.AreEqual(args.Insight.Confidence, 0.5);
                Assert.AreEqual(args.Insight.Magnitude, 0.5);
                Assert.LessOrEqual(args.Insight.CreatedTime, DateTime.UtcNow);
                Assert.Greater(args.Insight.CloseTime, DateTime.UtcNow);
                Assert.AreEqual(args.Insight.CreatedTime.AddSeconds((double)args.Insight.Period), args.Insight.CloseTime);
            };

            client.HeartbeatReceived += (sender, args) =>
            {
                Assert.AreEqual(args.AlphaId, TestAlphaId);
                Assert.AreEqual(args.AlgorithmId, "A-c2d57f0f051be64051a172bb27f1f5b6");
                Assert.LessOrEqual(args.MachineTime, DateTime.UtcNow);
            };

            client.OrderReceived += (sender, args) =>
            {
                Console.WriteLine(args.Order.ToString());
                var events = args.Order.OrderEvents;
            };

            client.AddAlphaStream(new AddAlphaStreamRequest { AlphaId = TestAlphaId });

            Thread.Sleep(60000);
            client.Dispose();

            var unsubscribeRequest = new UnsubscribeRequest { Id = TestAlphaId };
            var unsubscribeResponse = restClient.Execute(unsubscribeRequest).ConfigureAwait(false);
        }
    }
}