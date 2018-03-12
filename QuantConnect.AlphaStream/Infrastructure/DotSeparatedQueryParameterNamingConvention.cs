using System.Collections.Generic;
using System.Reflection;
using System.Runtime.Serialization;
using Newtonsoft.Json;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Defines the 'dot separated' naming convention for complex query parameters.
    /// </summary>
    public class DotSeparatedQueryParameterNamingConvention : IQueryParameterNamingConvention
    {
        /// <summary>
        /// Creates an enumerable of parameters resolved from the specified value.
        /// In the typical case, properties are read from the value and each emitted
        /// as key/value pairs representing the desired query parameter name/value
        /// </summary>
        /// <param name="member">The member info corresponding to the specified value</param>
        /// <param name="value">The complex value to be decomposed into name/value pairs</param>
        /// <returns>An enumerable of all name/value pairs resolved from the specified complex query parameter value</returns>
        public IEnumerable<QueryParameterDescriptor> GetQueryNameValuePairs(MemberInfo member, object value)
        {
            var context = GetQueryParameterName(member);
            foreach (var descriptor in GetQueryNameValuePairs(value, context))
            {
                yield return descriptor;
            }
        }

        /// <summary>
        /// Recursive call that walks through properties and if they're complex type, then through their properties as well
        /// </summary>
        private IEnumerable<QueryParameterDescriptor> GetQueryNameValuePairs(object value, string context)
        {
            if (value == null)
            {
                yield break;
            }

            foreach (var property in value.GetType().GetProperties())
            {
                var propertyName = GetQueryParameterName(property);
                var name = context.Length > 0
                    ? $"{context}-{propertyName}"
                    : propertyName;

                var propertyValue = property.GetValue(value);
                if (property.PropertyType.IsClass && property.PropertyType != typeof(string))
                {
                    // recurse on complex sub-types
                    foreach (var descriptor in GetQueryNameValuePairs(propertyValue, name))
                    {
                        yield return descriptor;
                    }
                }
                else
                {
                    yield return new QueryParameterDescriptor(name, propertyValue, property);
                }
            }
        }

        /// <summary>
        /// Resolves the query parameter name to use from attributes, defaulting to the member name if none found
        /// </summary>
        private string GetQueryParameterName(MemberInfo property)
        {
            var queryParameterAttribute = property.GetCustomAttribute<QueryParameterAttribute>();
            if (queryParameterAttribute != null)
            {
                return queryParameterAttribute.Name;
            }

            var jsonPropertyAttribute = property.GetCustomAttribute<JsonPropertyAttribute>();
            if (jsonPropertyAttribute != null)
            {
                return jsonPropertyAttribute.PropertyName;
            }

            var dataMemberAttribute = property.GetCustomAttribute<DataMemberAttribute>();
            if (dataMemberAttribute != null)
            {
                return dataMemberAttribute.Name;
            }

            return property.Name;
        }
    }
}