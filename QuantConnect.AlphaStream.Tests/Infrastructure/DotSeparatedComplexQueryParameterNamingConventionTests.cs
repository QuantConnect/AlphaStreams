using System.Linq;
using System.Runtime.Serialization;
using Newtonsoft.Json;
using NUnit.Framework;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream.Tests.Infrastructure
{
    [TestFixture]
    public class DotSeparatedComplexQueryParameterNamingConventionTests
    {
        [Test]
        public void HandlesComplexNestedTypes()
        {
            var value = new Request
            {
                Outter = new Outter
                {
                    Middle = new Middle
                    {
                        Inner = new Inner
                        {
                            Value = "my-value"
                        }
                    }
                }
            };

            var convention = new DotSeparatedQueryParameterNamingConvention();

            var member = typeof(Request).GetProperty(nameof(Request.Outter));
            var parameters = convention.GetQueryNameValuePairs(member, value.Outter).ToList();
            Assert.AreEqual(1, parameters.Count);
            Assert.AreEqual("outter-name.middle-name.inner-name.Value", parameters[0].Name);
            Assert.AreEqual(value.Outter.Middle.Inner.Value, parameters[0].Value);
            Assert.AreEqual(typeof(Inner).GetProperty(nameof(Inner.Value)), parameters[0].Member);
        }

        private class Request
        {
            // extra attributes test/document order of precedence when resolving the parameter name
            [QueryParameter("outter-name")]
            [JsonProperty("wrong-outter-name")]
            [DataMember(Name = "wrong-outter-name")]
            public Outter Outter { get; set; }
        }

        private class Outter
        {
            [JsonProperty("middle-name")]
            [DataMember(Name = "wrong-middle-name")]
            public Middle Middle { get; set; }
        }

        private class Middle
        {
            [DataMember(Name = "inner-name")]
            public Inner Inner { get; set; }
        }

        private class Inner
        {
            public string Value { get; set; }
        }
    }
}
