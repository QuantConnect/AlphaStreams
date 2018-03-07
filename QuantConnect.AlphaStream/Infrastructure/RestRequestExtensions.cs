using System.Collections.Generic;
using System.Linq;
using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Provides extension methods on <see cref="IRestRequest"/>
    /// </summary>
    public static class RestRequestExtensions
    {
        /// <summary>
        /// Gets the single parameter of tpe <see cref="ParameterType.RequestBody"/> or null if none found.
        /// </summary>
        /// <param name="request">The rest request object</param>
        /// <returns>The body parameter's value or null</returns>
        public static string GetBody(this IRestRequest request)
        {
            var body = request.GetParameters(ParameterType.RequestBody).SingleOrDefault();
            return body?.Value.ToString();
        }

        /// <summary>
        /// Gets all parameters of the specified type
        /// </summary>
        /// <param name="request">The rest request object</param>
        /// <param name="type">The parameter type to seach for</param>
        /// <returns>An enumerable of the matching parameters</returns>
        public static IEnumerable<Parameter> GetParameters(this IRestRequest request, ParameterType type)
        {
            return request.Parameters.Where(p => p.Type == type);
        }

        /// <summary>
        /// Combines the path and query together into the string that will be used when the request is executed
        /// </summary>
        /// <param name="request">The rest request object</param>
        /// <returns>The combined path and query from the rest request object</returns>
        public static string GetPathAndQuery(this IRestRequest request)
        {
            var resource = request.Resource;

            // replace path parameters
            foreach (var urlSegment in request.GetParameters(ParameterType.UrlSegment))
            {
                resource = resource.Replace($"{{{urlSegment.Name}}}", urlSegment.Value.ToString());
            }

            // construct query string
            var query = request.GetParameters(ParameterType.QueryString).Aggregate((string) null, (c, p) => $"{c + "?" ?? "?"}{p.Name}={p.Value}");

            return $"{resource}{query}";
        }
    }
}
