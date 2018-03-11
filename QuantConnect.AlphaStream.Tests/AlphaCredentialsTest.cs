using NUnit.Framework;

namespace QuantConnect.AlphaStream.Tests
{
    [TestFixture]
    public class AlphaCredentialsTests
    {
        [Test]
        public void CreatesSecureHash()
        {
            const long stamp = 1234567890L;
            var credentials = new AlphaCredentials("client-id", "api-token");
            var hash = credentials.CreateSecureHash(stamp);
            Assert.AreEqual("c2f75992e7ada8e6c985b830ed5ce12065c1f7ebd0a84feac6447b9cce185f0b", hash);
        }
    }
}
