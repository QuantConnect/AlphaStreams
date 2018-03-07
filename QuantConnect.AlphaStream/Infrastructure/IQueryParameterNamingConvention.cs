using System.Collections.Generic;
using System.Reflection;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Defines a naming convention for projecting a complex type into a query string.
    /// </summary>
    public interface IQueryParameterNamingConvention
    {
        /// <summary>
        /// Creates an enumerable of parameters resolved from the specified value.
        /// In the typical case, properties are read from the value and each emitted
        /// as key/value pairs representing the desired query parameter name/value
        /// </summary>
        /// <param name="member">The member info corresponding to the specified value</param>
        /// <param name="value">The complex value to be decomposed into name/value pairs</param>
        /// <returns>An enumerable of all name/value pairs resolved from the specified complex query parameter value</returns>
        IEnumerable<QueryParameterDescriptor> GetQueryNameValuePairs(MemberInfo member, object value);
    }
}