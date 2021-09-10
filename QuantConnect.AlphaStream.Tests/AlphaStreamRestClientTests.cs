using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using NUnit.Framework;
using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using QuantConnect.AlphaStream.Models.Orders;
using QuantConnect.AlphaStream.Requests;
using QuantConnect.Orders;
using Range = QuantConnect.AlphaStream.Models.Range;

namespace QuantConnect.AlphaStream.Tests
{
    [TestFixture]
    public class AlphaStreamRestClientTests
    {
        const string TestAlphaId = "d0fc88b1e6354fe95eb83225a";
        const string TestAuthorId = "2b2552a1c05f83ba4407d4c32889c367";
        private AlphaStreamRestClient _client;

        [SetUp]
        public void SetUp()
        {
            _client = new AlphaStreamRestClient(Credentials.Test);
        }

        [Test]
        public async Task GetsAlphaById()
        {
            var response = _client.GetAlphaById(TestAlphaId);
            Assert.IsNotNull(response);
            Assert.AreEqual(response.Id, TestAlphaId);
        }


        [Test]
        public async Task GetAlphaInsights()
        {
            var start = 0;
            var insights = new List<AlphaStreamInsight>() { };
            while (start < 500)
            {
                var response = _client.GetAlphaInsights(TestAlphaId, start);
                insights.AddRange(response);
                start += 100;
            }
            for (var i = 0; i <= insights.Count - 2; i++)
            {
                foreach (var insight in insights.GetRange(i + 1, insights.Count - i - 1))
                {
                    Assert.LessOrEqual(insights[i].GeneratedTimeUtc, insight.GeneratedTimeUtc);
                }
            }
            Assert.IsNotNull(insights);
            Assert.IsNotEmpty(insights);
        }

        [Test]
        public async Task GetAlphaOrders()
        {
            var start = 0;
            var orders = new List<AlphaStreamOrder>();
            while (start < 300)
            {
                var response = _client.GetAlphaOrders(TestAlphaId, start);
                orders.AddRange(response);
                start += 100;
            }
            for (var i = 0; i <= orders.Count - 2; i++)
            {
                foreach (var order2 in orders.GetRange(i + 1, orders.Count - i - 1))
                {
                    Assert.LessOrEqual(orders[i].CreatedTime, order2.CreatedTime);
                }

                var order = orders[i];
                Assert.AreNotEqual(OrderStatus.None, order.Status);
                Assert.AreNotEqual(0, order.Symbol.Length);
                Assert.AreNotEqual(0, order.AlgorithmId.Length);
                Assert.AreNotEqual(0, order.OrderId);
                Assert.AreNotEqual(0, order.SubmissionLastPrice);
                Assert.AreNotEqual(0, order.SubmissionAskPrice);
                
                Assert.AreNotEqual(0, order.SubmissionBidPrice);
                Assert.AreNotEqual(Source.LiveTrading, order.Source);

                if (order.Type != OrderType.Market
                    && order.Type != OrderType.MarketOnClose
                    && order.Type != OrderType.MarketOnOpen
                    && order.Status != OrderStatus.Filled)
                {
                    Assert.AreNotEqual(0, order.Price);
                }

                if (order.Status == OrderStatus.Filled)
                {
                    var orderEvent = order.OrderEvents.Last();
                    Assert.IsTrue(orderEvent.Status == OrderStatus.Filled);
                    Assert.AreNotEqual(0, orderEvent.FillPrice);
                    Assert.AreNotEqual(0, orderEvent.FillPriceCurrency.Length);
                }
                else if (order.Status == OrderStatus.Canceled)
                {
                    var orderEvent = order.OrderEvents.Last();
                    Assert.IsTrue(orderEvent.Status == OrderStatus.Canceled);
                }
                Assert.IsFalse(order.OrderEvents.Any(orderEvent => orderEvent.Quantity == 0));
                if (order.Type == OrderType.Limit || order.Type == OrderType.StopLimit)
                {
                    Assert.IsFalse(order.OrderEvents.Any(orderEvent => orderEvent.LimitPrice == 0));
                }
                if (order.Type == OrderType.StopMarket || order.Type == OrderType.StopLimit)
                {
                    Assert.IsFalse(order.OrderEvents.Any(orderEvent => orderEvent.StopPrice == 0));
                }
            }
            Assert.IsNotNull(orders);
            Assert.IsNotEmpty(orders);
        }

        [Test]
        public async Task GetAuthorById()
        {
            var response = _client.GetAuthorById(TestAuthorId);
            Assert.AreEqual(response.Id, TestAuthorId);
            Assert.AreEqual(response.Language, Language.CSharp);
        }

        [Test]
        public async Task GetAlphaTags()
        {
            var response = _client.GetAlphaTags().FindAll(t => t.TagName != "hidden");
            Assert.IsNotNull(response);
            Assert.GreaterOrEqual(response.Count, 40);
            foreach (var tag in response)
            {
                Assert.Greater(tag.TagName.Length, 0);
                Assert.GreaterOrEqual(tag.Matches, 0);

                var start = 0;
                var hasData = true;
                var searchAlphasFound = new List<Alpha>();
                while (hasData)
                {
                    var searchAlphaRequest = new SearchAlphasRequest()
                    {
                        IncludedTags = new List<string> { tag.TagName },
                        Start = start
                    };
                    var searchAlphaResponse = await ExecuteRequest(searchAlphaRequest).ConfigureAwait(false);
                    if (searchAlphaResponse.Count < 100)
                        hasData = false;
                    searchAlphasFound.AddRange(searchAlphaResponse);
                    start += 100;
                }

                Assert.AreEqual(searchAlphasFound.Count, tag.Matches);
                foreach (var alpha in searchAlphasFound)
                {
                    Assert.Contains(tag.TagName, alpha.Tags);
                };
            }
        }

        [Test]
        public async Task GetAlphaErrors()
        {
            var response = _client.GetAlphaErrors("c98a822257cf2087e37fddff9");
            Assert.IsNotNull(response);
            Assert.IsNotEmpty(response);
            var first = response.FirstOrDefault();
            Assert.AreEqual(first.Error.Substring(0, 10), "Algorithm.");
            Assert.AreEqual(first.StackTrace.Substring(0, 10), "System.Exc");
        }

        [TestCase(false)]
        [TestCase(true)]
        public async Task GetAlphaEquityCurve(bool unified)
        {
            var response = _client.GetAlphaEquityCurveCSharp("f50519a3d2b2598960bcdb59d", unified: unified);
            Assert.IsNotNull(response);
            Assert.IsNotEmpty(response);

            var idCount = response.GroupBy(x => x.Id).Count();

            // If we request the unified equity curve, it will include data for more than one version
            if (unified)
            {
                Assert.Greater(idCount, 1);
                return;
            }

            Assert.AreEqual(1, idCount);

            var sampleGroupDictionary = response.GroupBy(x => x.Sample)
                .ToDictionary(k => k.Key, v => v.ToList());

            Assert.IsTrue(sampleGroupDictionary.TryGetValue("in sample", out var inSample));
            Assert.Greater(inSample.Count, 0);
        }

        [Test]
        public async Task GetAlphaList()
        {
            var response = _client.GetAlphaList();
            Assert.IsNotNull(response);
            Assert.IsNotEmpty(response);
        }

        [Test]
        public async Task SearchAlphas()
        {
            var request = new SearchAlphasRequest
            {
                AssetClasses = new List<SecurityType> {SecurityType.Crypto},
                Sharpe = Range.Create(1, 999999999d),
            };
            var response = _client.SearchAlphas(request);
            Assert.IsNotNull(response);
            Assert.IsNotEmpty(response);
        }

        [Test]
        public async Task SearchAuthors()
        {
            var request = new SearchAuthorsRequest
            {
                Languages = { "C#" },
                Location = "New York",
                Projects = Range.Create(5, int.MaxValue)
            };
            var response = _client.SearchAuthors(request);
            Assert.IsNotNull(response);
            Assert.IsNotEmpty(response);
        }

        [Test]
        public async Task CreateBid()
        {
            var createRequest = new CreateBidPriceRequest
            {
                Id = TestAlphaId,
                Allocation = 10000,
                Bid = 3,
                Period = 28,
                GoodUntil = DateTime.Now.AddDays(1).ToUnixTime()
            };
            var createResponse = _client.CreateBid(createRequest);
            Assert.IsNotNull(createResponse);
            Assert.IsTrue(createResponse.Success);
        }

        [Test]
        public async Task CreateGetAndRemoveBidById()
        {
            await CreateBid();

            var getResponse = _client.GetAlphaBid(TestAlphaId);
            Assert.IsNotNull(getResponse);

            // Success
            var removeResponse = _client.RemoveAlphaBid(TestAlphaId, getResponse.ActiveBid.Id);
            Assert.IsNotNull(removeResponse);
            Assert.IsTrue(removeResponse.Success);

            // Fails: bid already cancelled
            removeResponse = _client.RemoveAlphaBid(TestAlphaId, getResponse.ActiveBid.Id);
            Assert.IsNotNull(removeResponse);
            Assert.IsFalse(removeResponse.Success);
            Assert.AreEqual(removeResponse.Messages.First(), "Bid already cancelled");

            // Fail: bid not found
            removeResponse = _client.RemoveAlphaBid(TestAlphaId, 123);
            Assert.IsNotNull(removeResponse);
            Assert.IsFalse(removeResponse.Success);
            Assert.AreEqual(removeResponse.Messages.First(), "Bid not found");
        }

        private static async Task<T> ExecuteRequest<T>(IRequest<T> request)
        {
            var service = new AlphaStreamRestClient(Credentials.Test);
            return await service.Execute(request).ConfigureAwait(false);
        }
    }
}