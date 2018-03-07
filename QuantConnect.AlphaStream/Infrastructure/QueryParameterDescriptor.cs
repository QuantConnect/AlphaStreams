using System.Reflection;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Provides information about a query parameter, including it's name, value and possibly
    /// the member that produced the value, such as a property info object.
    /// </summary>
    public class QueryParameterDescriptor
    {
        public string Name { get; }
        public object Value { get; }
        public MemberInfo Member { get; }

        /// <summary>
        /// Initializes a new instance of the <see cref="QueryParameterDescriptor"/> class
        /// </summary>
        /// <param name="name">The query parameter name</param>
        /// <param name="value">The query parameter value</param>
        /// <param name="member">The member info where the value came from</param>
        public QueryParameterDescriptor(string name, object value, MemberInfo member)
        {
            Name = name;
            Value = value;
            Member = member;
        }
    }
}