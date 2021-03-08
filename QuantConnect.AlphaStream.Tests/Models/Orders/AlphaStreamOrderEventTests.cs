using System;
using Newtonsoft.Json;
using NUnit.Framework;
using QuantConnect.AlphaStream.Models.Orders;
using QuantConnect.Orders;

namespace QuantConnect.AlphaStream.Tests.Models.Orders
{
    [TestFixture]
    public class AlphaStreamOrderEventTests
    {
        [Test]
        public void RoundTrip()
        {
            var orderEvent = new AlphaStreamOrderEvent
            {
                AlgorithmId = "AlgoId",
                Direction = OrderDirection.Buy,
                FillPrice = 10,
                FillPriceCurrency = "USD",
                FillQuantity = 1,
                IsAssignment = false,
                Message = "Broker message",
                OrderEventId = 9,
                Time = Time.DateTimeToUnixTimeStamp(DateTime.UtcNow),
                Symbol = "SPY",
                HashId = "MyHash"
            };
            AssertJsonRoundTrip(orderEvent);
        }

        [Test]
        public void OrderFee()
        {
            var orderEvent = new AlphaStreamOrderEvent
            {
                AlgorithmId = "AlgoId",
                Direction = OrderDirection.Buy,
                FillPrice = 10,
                FillPriceCurrency = "USD",
                FillQuantity = 1,
                IsAssignment = false,
                Message = "Broker message",
                OrderEventId = 9,
                Time = Time.DateTimeToUnixTimeStamp(DateTime.UtcNow),
                Symbol = "SPY",
                OrderFeeCurrency = "USD",
                OrderFeeAmount = 99,
                HashId = "MyHash"
            };
            AssertJsonRoundTrip(orderEvent);
        }

        [Test]
        public void LimitStopPrice()
        {
            var orderEvent = new AlphaStreamOrderEvent
            {
                AlgorithmId = "AlgoId",
                Direction = OrderDirection.Buy,
                FillPrice = 10,
                FillPriceCurrency = "USD",
                FillQuantity = 1,
                IsAssignment = false,
                Message = "Broker message",
                OrderEventId = 9,
                Time = Time.DateTimeToUnixTimeStamp(DateTime.UtcNow),
                Symbol = "SPY",
                LimitPrice = 80,
                StopPrice = 100,
                HashId = "MyHash"
            };
            AssertJsonRoundTrip(orderEvent);
        }

        public void AssertJsonRoundTrip(AlphaStreamOrderEvent orderEvent)
        {
            var serialization = JsonConvert.SerializeObject(orderEvent);
            var deserialization = JsonConvert.DeserializeObject<AlphaStreamOrderEvent>(serialization);

            Assert.AreEqual(orderEvent.FillPrice, deserialization.FillPrice);
            Assert.AreEqual(orderEvent.FillPriceCurrency, deserialization.FillPriceCurrency);
            Assert.AreEqual(orderEvent.OrderEventId, deserialization.OrderEventId);
            Assert.AreEqual(orderEvent.HashId, deserialization.HashId);
            Assert.AreEqual(orderEvent.OrderFeeAmount, deserialization.OrderFeeAmount);
            Assert.AreEqual(orderEvent.OrderFeeCurrency, deserialization.OrderFeeCurrency);
            Assert.AreEqual(orderEvent.IsAssignment, deserialization.IsAssignment);
            Assert.AreEqual(orderEvent.Symbol, deserialization.Symbol);
            Assert.AreEqual(orderEvent.Message, deserialization.Message);
            Assert.AreEqual(orderEvent.FillQuantity, deserialization.FillQuantity);
            Assert.AreEqual(orderEvent.Direction, deserialization.Direction);
            Assert.AreEqual(orderEvent.Status, deserialization.Status);
            Assert.AreEqual(orderEvent.Id, deserialization.Id);
            Assert.AreEqual(orderEvent.StopPrice, deserialization.StopPrice);
            Assert.AreEqual(orderEvent.LimitPrice, deserialization.LimitPrice);
            Assert.AreEqual(orderEvent.Time, deserialization.Time, 10000);
            Assert.AreEqual(orderEvent.Quantity, deserialization.Quantity);
        }
    }
}
