using System;
using NUnit.Framework;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream.Tests.Infrastructure
{
    [TestFixture]
    public class TimeTests
    {
        [Test]
        public void CreatesCorrectUnixTimeStamp()
        {
            var now = new DateTime(2000, 01, 01);
            var stamp = now.ToUnixTime();
            Assert.AreEqual(946684800, stamp);
        }
    }
}
