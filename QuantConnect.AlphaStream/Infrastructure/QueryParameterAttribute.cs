using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Web;
using Newtonsoft.Json;
using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Defines a parameter as part of the query string
    /// </summary>
    public class QueryParameterAttribute : ParameterAttribute
    {
        // cache of resolved json converter instances
        private static readonly Dictionary<MemberInfo, JsonConverter> JsonConvertersByMemberInfo = new Dictionary<MemberInfo, JsonConverter>();

        private readonly IQueryParameterNamingConvention parameterNamingConvention;

        /// <summary>
        /// Initializes a new insance of the <see cref="QueryParameterAttribute"/> class
        /// </summary>
        /// <param name="name">The query parameter name</param>
        /// <param name="complexParameterNamingConventionType">A naming convention used for projecting complex
        /// types into name/value pairs for the query string. Specify null to use the default <see cref="HyphenSeparatedQueryParameterNamingConvention"/></param>
        public QueryParameterAttribute(string name, Type complexParameterNamingConventionType = null)
            : base(name)
        {
            complexParameterNamingConventionType = complexParameterNamingConventionType ?? typeof(HyphenSeparatedQueryParameterNamingConvention);
            parameterNamingConvention = (IQueryParameterNamingConvention) Activator.CreateInstance(complexParameterNamingConventionType);
        }

        /// <summary>
        /// Set the parameter on the request object in the query string
        /// </summary>
        /// <param name="request">The rest request object</param>
        /// <param name="member">The member of the value</param>
        /// <param name="value">The value to be added as a parameter</param>
        public override void SetParameter(IRestRequest request, MemberInfo member, object value)
        {
            if (ReferenceEquals(null, value))
            {
                return;
            }

            // string values can be added directly to the request
            var str = value as string;
            if (str != null)
            {
                AddQueryParameter(request, Name, str);
                return;
            }

            // enumerables in query parameters are formed as multiple parameters w/ the same name
            var enumerable = value as IEnumerable;
            if (enumerable != null)
            {
                str = string.Join(",", enumerable.OfType<object>().Select(v => Convert(member, v)));
                if (!string.IsNullOrEmpty(str))
                {
                    AddQueryParameter(request, Name, str);
                }
                return;
            }

            if (value.GetType().IsClass)
            {
                // decompose complex types using the configured naming convention
                foreach (var descriptor in parameterNamingConvention.GetQueryNameValuePairs(member, value))
                {
                    // no point in sending nulls in the query string
                    if (descriptor.Value == null)
                    {
                        continue;
                    }

                    var parameterValue = Convert(descriptor.Member, descriptor.Value);
                    AddQueryParameter(request, descriptor.Name, parameterValue);
                }
            }
            else
            {
                var parameterValue = Convert(member, value);
                AddQueryParameter(request, Name, parameterValue);
            }
        }

        /// <summary>
        /// Converts the value according to the member. Checks for JsonConverter attribute.
        /// </summary>
        private string Convert(MemberInfo member, object value)
        {
            if (value is bool)
            {
                return value.ToString().ToLower();
            }

            // check if the member defines a json converter
            JsonConverter jsonConverter;
            if (!JsonConvertersByMemberInfo.TryGetValue(member, out jsonConverter))
            {
                // check the member then the value's type for a registered converter
                var jsonConverterAttribute = member.GetCustomAttribute<JsonConverterAttribute>()
                    ?? value.GetType().GetCustomAttribute<JsonConverterAttribute>();

                if (jsonConverterAttribute != null)
                {
                    // instantiate the json converter from the attribute definition
                    jsonConverter = (JsonConverter) Activator.CreateInstance(
                        jsonConverterAttribute.ConverterType,
                        jsonConverterAttribute.ConverterParameters
                    );
                }

                // save to mapping even if null, only need to figure out it doesn't exist once
                JsonConvertersByMemberInfo[member] = jsonConverter;
            }

            // no json converter configured, simply use to string
            if (jsonConverter == null)
            {
                return value.ToString();
            }

            // convert the value using the configured json converter
            using (var stringWriter = new StringWriter())
            using (var jsonWriter = new JsonTextWriter(stringWriter))
            {
                var serializer = new JsonSerializer();
                jsonConverter.WriteJson(jsonWriter, value, serializer);

                // serializer will write it as if it's being placed in json, so
                // string values will end up within quotes that we need to remove
                return stringWriter.GetStringBuilder().ToString().TrimStart('"').TrimEnd('"');
            }
        }

        /// <summary>
        /// Adds the query parameter to the request after performing url encoding
        /// </summary>
        private void AddQueryParameter(IRestRequest request, string name, object value)
        {
            request.AddQueryParameter(name, value.ToString());
        }
    }
}