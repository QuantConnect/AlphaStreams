using System.Collections.Generic;
using System.Text;
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

        /// <summary>
        /// Returns a string that represents the ApiResponse object
        /// </summary>
        /// <returns>A string that represents the Alpha object</returns>
        public override string ToString()
        {
            if (Success)
            {
                return "Successful response from the API";
            }

            var stringBuilder = new StringBuilder("Failed response from the API: ");
            if (string.IsNullOrWhiteSpace(Message))
            {
                stringBuilder.Append(Message);
            }

            if (Messages.Count > 0)
            {
                stringBuilder.Append(string.Join(", ", Messages));
            }

            return stringBuilder.ToString();
        }
    }
}