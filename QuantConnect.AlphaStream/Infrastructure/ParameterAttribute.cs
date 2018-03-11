using System;
using System.Reflection;
using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Defines a parameter in a request
    /// </summary>
    [AttributeUsage(AttributeTargets.Property)]
    public abstract class ParameterAttribute : Attribute
    {
        /// <summary>
        /// Gets the name of this parameter
        /// </summary>
        public string Name { get; }

        /// <summary>
        /// Initializes a new instance of the <see cref="ParameterAttribute"/> class
        /// </summary>
        /// <param name="name">The name of the parameter</param>
        protected ParameterAttribute(string name)
        {
            Name = name;
        }

        /// <summary>
        /// Set the parameter on the request object
        /// </summary>
        /// <param name="request">The rest request object</param>
        /// <param name="member">The member of the value</param>
        /// <param name="value">The value to be added as a parameter</param>
        public abstract void SetParameter(IRestRequest request, MemberInfo member, object value);
    }
}