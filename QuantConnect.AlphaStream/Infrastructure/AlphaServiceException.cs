using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using Newtonsoft.Json;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Exception thrown while communicating with the QuantConnect Alpha Streams REST Service.
    /// </summary>
    public class AlphaServiceException : Exception
    {
        /// <summary>
        /// The resposne content.
        /// </summary>
        public string Content { get; }

        /// <summary>
        /// The response status code.
        /// </summary>
        public HttpStatusCode StatusCode { get; }

        /// <summary>
        /// Error messages includes with the response.
        /// </summary>
        public List<string> Messages { get; } = new List<string>();

        public AlphaServiceException(string message, HttpStatusCode statusCode, string content, IEnumerable<string> messages)
            : base(message)
        {
            Content = content;
            StatusCode = statusCode;
            Messages.AddRange(messages);
        }

        public static AlphaServiceException ForResponse(IRestResponse response)
        {
            var messages = new List<string>();
            try
            {
                // try to parse as a generic api response and add error messages
                var apiResonse = JsonConvert.DeserializeObject<ApiResponse>(response.Content);
                if (apiResonse?.Messages?.Count > 0)
                {
                    foreach (var message in apiResonse.Messages)
                    {
                        messages.Add(message);
                        Trace.TraceError(message);
                    }
                }
            }
            catch
            {
            }

            var msg = messages.Any() ? messages[0] : "Received an unexpected response from the server.";
            return new AlphaServiceException(msg, response.StatusCode, response.Content, messages);
        }
    }
}