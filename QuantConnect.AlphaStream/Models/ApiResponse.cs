using System.Collections.Generic;
using Newtonsoft.Json;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Generic success/error response message from the API.
    /// </summary>
    public class ApiResponse
    {
        /// <summary>
        /// Boolean indicating success
        /// </summary>
        [JsonProperty("success")]
        public bool Success { get; set; }

        /// <summary>
        /// Single message from the API.
        /// </summary>
        [JsonProperty("message")]
        public string Message { get; set; }

        /// <summary>
        /// Array of error messages from the API.
        /// </summary>
        [JsonProperty("messages")]
        public List<string> Messages { get; set; } = new List<string>();
    }
}