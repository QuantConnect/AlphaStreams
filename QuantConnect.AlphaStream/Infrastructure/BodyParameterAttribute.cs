using System;
using System.Linq;
using System.Reflection;
using Newtonsoft.Json.Linq;
using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    [AttributeUsage(AttributeTargets.Property)]
    public class BodyParameterAttribute : ParameterAttribute
    {
        public BodyParameterAttribute(string name)
            : base(name)
        {
        }

        public override void SetParameter(IRestRequest request, MemberInfo member, object value)
        {
            if (value == null)
            {
                return;
            }

            var jtoken = JToken.FromObject(value);
            var body = request.Parameters.SingleOrDefault(p => p.Type == ParameterType.RequestBody);
            if (body == null)
            {
                var jobject = new JObject
                {
                    [Name] = jtoken
                };
                request.AddParameter("application/json", jobject, "application/json", ParameterType.RequestBody);
            }
            else
            {
                // update the request body to include this new property
                var bodyJToken = body.Value is JObject ? (JObject) body.Value : JObject.Parse(body.Value.ToString());
                bodyJToken[Name] = jtoken;
                body.Value = bodyJToken;
            }
        }
    }
}