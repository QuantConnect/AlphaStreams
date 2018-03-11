using System;
using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Specifies an endpoint for a REST request
    /// </summary>
    [AttributeUsage(AttributeTargets.Class)]
    public class EndpointAttribute : Attribute
    {
        /// <summary>
        /// Gets the <see cref="Method"/> for this endpoint
        /// </summary>
        public Method Method { get; }

        /// <summary>
        /// Gets the resource path
        /// </summary>
        public string Resource { get; }

        /// <summary>
        /// Initializes a new instance of the <see cref="EndpointAttribute"/> class
        /// </summary>
        /// <param name="method">The HTTP verb</param>
        /// <param name="resource">The resource path</param>
        public EndpointAttribute(Method method, string resource)
        {
            Method = method;
            Resource = resource;
        }
    }
}