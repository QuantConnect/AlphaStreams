using System;
using System.Linq;
using System.Reflection;
using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Rest request object that uses attributes to define the endpoint and parameters of the request
    /// </summary>
    /// <typeparam name="T">The expected response type from the server</typeparam>
    public abstract class AttributeRequest<T> : IRequest<T>
    {
        /// <summary>
        /// Converts this request object into a rest sharp request object.
        /// </summary>
        /// <returns>The rest sharp request object</returns>
        public IRestRequest ToRestRequest()
        {
            var type = GetType();

            // resolve endpoint
            var endpoint = type.GetCustomAttribute<EndpointAttribute>();
            if (endpoint == null)
            {
                throw new InvalidOperationException($"Request types must be decorated with the {nameof(EndpointAttribute)}.");
            }

            // resolve parameters from request object
            var parameters = type.GetProperties().Select(p => new
            {
                property = p,
                parameter = p.GetCustomAttribute<ParameterAttribute>()
            });

            // apply parameters from request object to rest request
            var restRequest = new RestRequest(endpoint.Resource, endpoint.Method);
            foreach (var item in parameters.Where(item => item.parameter != null))
            {
                // resolve parameter value
                var value = item.property.GetValue(this);

                // set parameter on rest request
                item.parameter.SetParameter(restRequest, item.property, value);
            }

            return restRequest;
        }
    }
}