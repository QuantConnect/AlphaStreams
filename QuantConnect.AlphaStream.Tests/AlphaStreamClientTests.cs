using System;
using System.Linq;
using System.Threading;
using NUnit.Framework;
using QuantConnect.Algorithm.Framework.Alphas;
using QuantConnect.AlphaStream.Models;
using QuantConnect.AlphaStream.Requests;
using QuantConnect.Orders;

namespace QuantConnect.AlphaStream.Tests
{
    [TestFixture]
    public class AlphaStreamClientTests
    {
        [Test]
        public void StreamTest()
        {
            const string testAlphaId = "79e963f0f1160ff5789450b09";

            // set credentials for connecting to your alpha streams exchange
            var info = new AlphaStreamCredentials(
                "35.231.13.1",
                5672,
                "quantconnect_test",
                "",
                "QCAlphaExchange_quantconnect_test",
                "quantconnect_test"
            );

            var client = new AlphaStreamEventClient(info);
            client.Connect();

            client.InsightReceived += (sender, args) =>
            {
                Assert.AreEqual(args.Insight.Direction, InsightDirection.Flat);
                Assert.AreEqual(args.Insight.Source, Source.LiveTrading);
                Assert.AreEqual(args.Insight.Period, Time.OneMinute);
                Assert.AreEqual(args.Insight.Symbol.ID.ToString(), "EURUSD 8G");
                Assert.AreEqual(args.Insight.Type, InsightType.Price);
                Assert.AreEqual(args.Insight.SourceModel, "eef0aede-d827-454c-ab61-c3e410cdd449");
                Assert.IsNull(args.Insight.Weight);
                Assert.IsNull(args.Insight.Confidence);
                Assert.IsNull(args.Insight.Magnitude);
                Assert.LessOrEqual(args.Insight.GeneratedTimeUtc, DateTime.UtcNow);
                Assert.Greater(args.Insight.CloseTimeUtc, DateTime.UtcNow);
                Assert.AreEqual(args.Insight.GeneratedTimeUtc.Add(args.Insight.Period), args.Insight.CloseTimeUtc);
            };

            client.HeartbeatReceived += (sender, args) =>
            {
                Assert.LessOrEqual(args.MachineTime, DateTime.UtcNow);
                Assert.AreEqual(args.AlphaId, testAlphaId);
                Assert.AreEqual(args.AlgorithmId, "A-a0b454181d0ec497d2989453a79b16c9");
            };

            client.OrderReceived += (sender, args) =>
            {
                Assert.AreNotEqual(args.Order.Direction, OrderDirection.Hold);
                Assert.AreEqual(args.Order.Source, Source.LiveTrading);
                Assert.AreEqual(args.Order.AlgorithmId, "A-a0b454181d0ec497d2989453a79b16c9");
                Assert.AreEqual(args.Order.Symbol, "EURUSD 8G");
                var events = args.Order.OrderEvents;
                Assert.GreaterOrEqual(events.Count, 0);
                Assert.AreEqual(events.First().Symbol, "EURUSD 8G");
            };

            client.AddAlphaStream(new AddAlphaStreamRequest { AlphaId = testAlphaId });

            Thread.Sleep(60000);
            client.Dispose();
        }
    }
}