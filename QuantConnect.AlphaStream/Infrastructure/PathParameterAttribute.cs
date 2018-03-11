using System;
using System.Collections;
using System.Reflection;
using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Defines a parameter as part of the url path
    /// </summary>
    public class PathParameterAttribute : ParameterAttribute
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="PathParameterAttribute"/> class
        /// </summary>
        /// <param name="name">The name of the parameter</param>
        public PathParameterAttribute(string name)
            : base(name)
        {
        }

        /// <summary>
        /// Set the parameter on the request object in the url path
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

            if (value is string || !(value is IEnumerable))
            {
                request.AddUrlSegment(Name, value.ToString());
            }
            else
            {
                throw new ArgumentException("Path parameters must be scalar values.");
            }
        }
    }
}