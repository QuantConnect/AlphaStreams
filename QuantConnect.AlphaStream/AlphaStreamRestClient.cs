using System;
using System.Diagnostics;
using System.Net;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using QuantConnect.AlphaStream.Infrastructure;
using RestSharp;
using RestSharp.Authenticators;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Client used to communicate with alpha stream REST api
    /// </summary>
    public class AlphaStreamRestClient : IAlphaStreamRestClient
    {
        public static bool RequestTracingEnabled = false;
        public static bool ResponseTracingEnabled = false;
        public const string DefaultBaseUrl = "https://www.quantconnect.com/api/v2";

        private readonly IRestClient client;
        private readonly AlphaCredentials credentials;

        /// <summary>
        /// Initializes a new instance of the <see cref="AlphaStreamRestClient"/> class
        /// </summary>
        /// <param name="credentials">Credentials used to connect to the alpha streams rest service</param>
        public AlphaStreamRestClient(AlphaCredentials credentials)
            : this(DefaultBaseUrl, credentials)
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="AlphaStreamRestClient"/> class
        /// </summary>
        /// <param name="baseUrl">The base url used for making requests</param>
        /// <param name="credentials">Credentials used to connect to the alpha streams rest service</param>
        public AlphaStreamRestClient(string baseUrl, AlphaCredentials credentials)
            : this(new RestClient(baseUrl ?? DefaultBaseUrl), credentials)
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="AlphaStreamRestClient"/> class
        /// </summary>
        /// <param name="client">Rest client implementation.</param>
        /// <param name="credentials">Credentials used to connect to the alpha streams rest service</param>
        public AlphaStreamRestClient(IRestClient client, AlphaCredentials credentials)
        {
            this.client = client;
            this.credentials = credentials;
        }

        /// <summary>
        /// Executes the specified request against the alpha stream rest server
        /// </summary>
        /// <typeparam name="T">The response type</typeparam>
        /// <param name="request">The request object that will be transformed into a rest request</param>
        /// <returns>The response</returns>
        public async Task<T> Execute<T>(IRequest<T> request)
        {
            var restRequest = request.ToRestRequest();

            if (RequestTracingEnabled)
            {
                var pathAndQuery = client.BuildUri(restRequest).ToString().Replace(DefaultBaseUrl, string.Empty);
                Trace.TraceInformation($"{restRequest.Method} {pathAndQuery}");

                var body = restRequest.GetBody();
                if (body != null)
                {
                    Trace.TraceInformation($"Request Body: {Environment.NewLine}{body.FormatAsJsonIfPossible()}");
                }
            }

            // add required authorization headers
            var stamp = GetUnixTimeStamp();
            restRequest.AddHeader("Timestamp", stamp.ToString());
            client.Authenticator = new HttpBasicAuthenticator(
                credentials.ClientId,
                credentials.CreateSecureHash(stamp)
            );

            var taskCompletionSource = new TaskCompletionSource<JToken>();
            client.ExecuteAsync(restRequest, response =>
            {
                if (ResponseTracingEnabled)
                {
                    Trace.TraceInformation("Response Body: " + Environment.NewLine + response.Content.FormatAsJsonIfPossible());
                }

                if (response.StatusCode == HttpStatusCode.OK)
                {
                    try
                    {
                        taskCompletionSource.SetResult(JToken.Parse(response.Content));
                        return;
                    }
                    catch (Exception exception)
                    {
                        Trace.TraceError("Error Deserializing Response: " + Environment.NewLine + exception.ToString());
                    }
                }

                // either received a non 200 status code or failed to parse as the requested type
                taskCompletionSource.SetException(AlphaServiceException.ForResponse(response));
            });

            var jtokenResponse = await taskCompletionSource.Task.ConfigureAwait(false);
            return jtokenResponse.ToObject<T>();
        }

        /// <summary>
        /// Fetches the current UTC time in unix fractional seconds since epoch.
        /// This is provided as a test seam.
        /// </summary>
        /// <returns>The current time in unix fractional seconds since epoch</returns>
        protected long GetUnixTimeStamp()
        {
            return DateTime.UtcNow.ToUnixTime();
        }
    }
}