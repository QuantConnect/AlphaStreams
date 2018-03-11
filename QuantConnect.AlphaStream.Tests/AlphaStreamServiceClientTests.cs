using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using NUnit.Framework;
using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using QuantConnect.AlphaStream.Requests;

namespace QuantConnect.AlphaStream.Tests
{
    [TestFixture]
    public class AlphaStreamServiceClientTests
    {
        const string TestAlphaId = "623b06b231eb1cc1aa3643a46";
        const string TestAuthorId = "1f48359f6c6cbad65b091232eaae73ce";

        [Test]
        public async Task GetsAlphaById()
        {
            var request = new GetAlphaByIdRequest {Id = TestAlphaId};
            var response = await ExecuteRequest(request).ConfigureAwait(false);
            Assert.IsNotNull(response);
            Assert.AreEqual(response.Id, TestAlphaId);
        }

        [Test]
        public async Task GetAlphaInsights()
        {
            var request = new GetAlphaInsightsRequest {Id = TestAlphaId};
            var response = await ExecuteRequest(request).ConfigureAwait(false);
            Assert.IsNotNull(response);
            Assert.IsNotEmpty(response);
        }

        [Test]
        public async Task GetAuthorById()
        {
            var request = new GetAuthorByIdRequest {Id = TestAuthorId};
            var response = await ExecuteRequest(request).ConfigureAwait(false);
            Assert.AreEqual(response.Id, TestAuthorId);
            Assert.AreEqual(response.Language, "C#");
        }

        [Test]
        public async Task SearchAlphas()
        {
            var request = new SearchAlphasRequest
            {
                Assets = {AssetClass.Crypto},
                Accuracy = Range.Create(0d, null),
                Fee = Range.Create(0, decimal.MaxValue),
                Sharpe = Range.Create(0, double.MaxValue),
                // this is the quantconnect symbol security identifier string
                Symbols = new List<string> {"BTCUSD XJ"},
                Uniqueness = Range.Create(0, double.MaxValue)
            };
            var response = await ExecuteRequest(request).ConfigureAwait(false);
            Assert.IsNotNull(response);
            Assert.IsNotEmpty(response);
        }

        [Test]
        public async Task SearchAuthors()
        {
            var request = new SearchAuthorsRequest
            {
                Biography = "QuantConnect",
                Language = {"C#"},
                SignedUp = Range.Create(Time.UnixEpoch, DateTime.Today),
                Alphas = Range.Create(0, int.MaxValue),
                ForumComments = Range.Create(0, int.MaxValue),
                ForumDiscussions = Range.Create(0, int.MaxValue),
                LastLogin = Range.Create(Time.UnixEpoch, DateTime.Today),
                Projects = Range.Create(0, int.MaxValue)
            };
            var response = await ExecuteRequest(request).ConfigureAwait(false);
            Assert.IsNotNull(response);
            Assert.IsNotEmpty(response);
        }

        [Test]
        public async Task Subscribe()
        {
            var request = new SubscribeRequest { Id = TestAlphaId, Exclusive = false };
            var response = await ExecuteRequest(request).ConfigureAwait(false);
            Assert.IsNotNull(response);
            Assert.IsTrue(response.Success);
            Assert.IsEmpty(response.Messages);
        }

        [Test]
        public async Task Unubscribe()
        {
            var request = new UnsubscribeRequest { Id = TestAlphaId };
            var response = await ExecuteRequest(request).ConfigureAwait(false);
            Assert.IsNotNull(response);
            Assert.IsTrue(response.Success);
            Assert.IsEmpty(response.Messages);
        }

        private static async Task<T> ExecuteRequest<T>(IRequest<T> request)
        {
            var service = new AlphaStreamRestClient(Credentials.Test);
            return await service.Execute(request).ConfigureAwait(false);
        }
    }
}