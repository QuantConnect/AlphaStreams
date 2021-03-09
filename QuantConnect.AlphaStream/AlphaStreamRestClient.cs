using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using QuantConnect.AlphaStream.Models.Orders;
using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using QuantConnect.AlphaStream.Requests;
using RestSharp;
using RestSharp.Authenticators;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Client used to communicate with alpha stream REST api
    /// </summary>
    public class RequestTracingEnabled : IAlphaStreamRestClient
    {
        public static bool RequestTracingEnabled = false;
        public static bool ResponseTracingEnabled = false;
        public static string LastRestResponse = "";
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
        /// Get a specific Alpha by Id
        /// </summary>
        /// <param name="id">The Alpha Stream unique hash id</param>
        /// <returns></returns>
        public Alpha GetAlphaById(string id)
        {
            var request = new GetAlphaByIdRequest { Id = id };
            return Execute(request).Result;
        }

        /// <summary>
        /// Request all Alpha Stream Insights
        /// </summary>
        /// <param name="id">Alpha Id</param>
        /// <param name="startPosition">Position in the collection to fetch the next 100</param>
        /// <returns>List of insights from the alpha</returns>
        public List<AlphaStreamInsight> GetAlphaInsights(string id, int startPosition)
        {
            var request = new GetAlphaInsightsRequest { Id = id, Start = startPosition };
            var response = Execute(request).Result;

            return response;
        }

        /// <summary>
        /// Fetch an Alpha Streams order object infused with more information about the fills and time stamps
        /// </summary>
        /// <param name="id">Alpha id to download</param>
        /// <param name="startPosition">Starting position of the index.</param>
        /// <returns>List of Alpha Stream Order objects</returns>
        public List<AlphaStreamOrder> GetAlphaOrders(string id, int startPosition)
        {
            var request = new GetAlphaOrdersRequest { Id = id, Start = startPosition };
            return Execute(request).Result;
        }

        /// <summary>
        /// Get the author's information by the id of the author.
        /// </summary>
        /// <param name="authorId">Hash identity of the author</param>
        /// <returns>Author Alpha Stream object</returns>
        public Author GetAuthorById(string authorId)
        {
            var request = new GetAuthorByIdRequest { Id = authorId };
            return Execute(request).Result;
        }

        /// <summary>
        /// Get a list of all the tags used in Alpha Streams to know what to search for.
        /// </summary>
        /// <returns>string list of tags</returns>
        public List<Tag> GetAlphaTags()
        {
            var request = new GetAlphaTagsRequest();
            return Execute(request).Result;
        }

        /// <summary>
        /// List all the runtime errors of the alpha
        /// </summary>
        /// <param name="alphaId">Specific alpha to get the runtime errors for</param>
        /// <returns>List of runtime error objects</returns>
        public List<RuntimeError> GetAlphaErrors(string alphaId)
        {
            var request = new GetAlphaErrorsRequest { Id = alphaId };
            return Execute(request).Result;
        }

        /// <summary>
        /// Lists all the available alphas
        /// </summary>
        /// <returns></returns>
        public string[] GetAlphaList()
        {
            var request = new GetAlphaListRequest();
            return Execute(request).Result.ToArray();
        }

        /// <summary>
        /// Search the Alpha Streams for specific criteria
        /// </summary>
        /// <param name="request"></param>
        /// <returns></returns>
        public List<Alpha> SearchAlphas(SearchAlphasRequest request)
        {
            return Execute(request).Result;
        }

        /// <summary>
        /// Search the authors database for specific criteria
        /// </summary>
        /// <param name="request">Object with the search criteria</param>
        /// <returns>List of matching authors</returns>
        public List<Author> SearchAuthors(SearchAuthorsRequest request)
        {
            return Execute(request).Result;
        }

        /// <summary>
        /// Create a new bid for this alpha
        /// </summary>
        /// <param name="createRequest"></param>
        /// <returns></returns>
        public ApiResponse CreateBid(CreateBidPriceRequest createRequest)
        {
            return Execute(createRequest).Result;
        }

        /// <summary>
        /// Get a Bid for a specific Alpha
        /// </summary>
        /// <param name="id">The Alpha Stream unique hash id</param>
        public BidResult GetAlphaBid(string id)
        {
            var request = new GetAlphaBidRequest { Id = id };
            return Execute(request).Result;
        }

        /// <summary>
        /// Remove a Bid for a specific Alpha
        /// </summary>
        /// <param name="id">The Alpha Stream unique hash id</param>
        /// <param name="bidId">The bid unique id</param>
        public ApiResponse RemoveAlphaBid(string id, int bidId)
        {
            var request = new RemoveAlphaBidRequest {Id = id, BidId = bidId};
            return Execute(request).Result;
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
                    LastRestResponse = response.Content;
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