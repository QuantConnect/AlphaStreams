using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Request object that is convertible into a rest sharp request object.
    /// </summary>
    /// <typeparam name="T">Response type</typeparam>
    public interface IRequest<T>
    {
        /// <summary>
        /// Converts this request object into a rest sharp request object.
        /// </summary>
        /// <returns>The rest sharp request object</returns>
        IRestRequest ToRestRequest();
    }
}