namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Defines the required connection information for connection to alpha streams streaming server
    /// </summary>
    /// <remarks>Kept for backwards compatibility <see cref="AlphaStreamCredentials"/></remarks>
    public class AlphaInsightsStreamCredentials : AlphaStreamCredentials
    {
        public AlphaInsightsStreamCredentials(string hostName,
            int port,
            string username,
            string password,
            string exchangeName,
            string virtualHost = "/",
            bool automaticRecoveryEnabled = true,
            int requestedConnectionTimeout = 5000,
            string consumerTag = null)
        : base(hostName, port, username, password, exchangeName, virtualHost, automaticRecoveryEnabled, requestedConnectionTimeout, consumerTag)
        {
        }
    }
}