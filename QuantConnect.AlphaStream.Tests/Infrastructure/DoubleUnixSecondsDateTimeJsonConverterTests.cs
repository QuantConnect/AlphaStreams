using System;
using Newtonsoft.Json;
using NUnit.Framework;
using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Tests.Infrastructure
{
    [TestFixture]
    public class DoubleUnixSecondsDateTimeJsonConverterTests
    {
        private static readonly double DefaultDateTimeInDoubleUnixSeconds = default(DateTime).ToUnixTime();

        private static readonly JsonSerializerSettings SerializerSettings = new JsonSerializerSettings
        {
            Converters = { new DoubleUnixSecondsDateTimeJsonConverter() }
        };

        [Test]
        public void RoundTripsDateTimeAsDoubleSeconds()
        {
            var y2k = new DateTime(2000, 1, 1, 0, 0, 0, DateTimeKind.Utc).AddMilliseconds(122.99991);
            var target = new TargetType
            {
                DateTime = y2k,
                NullableDateTime = y2k
            };
            var json = JsonConvert.SerializeObject(target, SerializerSettings);

            Assert.AreEqual("{\"DateTime\":946684800.12299991,\"NullableDateTime\":946684800.12299991}", json);

            var deserialized = JsonConvert.DeserializeObject<TargetType>(json, SerializerSettings);
            Assert.AreEqual(target.DateTime, deserialized.DateTime);
            Assert.AreEqual(target.NullableDateTime, deserialized.NullableDateTime);
        }

        [Test]
        public void RoundTripsDefaultValues()
        {
            var y2k = new DateTime(2000, 1, 1, 0, 0, 0, DateTimeKind.Utc).AddMilliseconds(122.99991);
            var target = new TargetType
            {
                DateTime = default(DateTime),
                NullableDateTime = default(DateTime?)
            };
            var json = JsonConvert.SerializeObject(target, SerializerSettings);

            // without specifying ignore default values, will serialize default(DateTime) just as any other date time value
            Assert.AreEqual($"{{\"DateTime\":{DefaultDateTimeInDoubleUnixSeconds:.0},\"NullableDateTime\":null}}", json);

            var deserialized = JsonConvert.DeserializeObject<TargetType>(json, SerializerSettings);
            Assert.AreEqual(target.DateTime, deserialized.DateTime);
            Assert.AreEqual(target.NullableDateTime, deserialized.NullableDateTime);
        }

        class TargetType
        {
            public DateTime DateTime { get; set; }
            public DateTime? NullableDateTime { get; set; }
        }
    }
}
