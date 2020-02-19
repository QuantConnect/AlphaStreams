using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream.Models
{
    public class Conversation
    {
        // <summary>
        /// Subject line of the message
        /// </summary>
        [JsonProperty("subject")]
        public string Subject { get; set; }

        /// <summary>
        /// Contents of the message
        /// </summary>
        [JsonProperty("message")]
        public string Message { get; set; }

        /// <summary>
        /// Dictionary of message sender information keyed by the type of information.
        /// If the key is 'id', From returns the sender anonymized hash id.
        /// If the key is "type", From returns the type of the sender, either "client" or "author"
        /// </summary>
        [JsonProperty("from")]
        public Dictionary<string, string> From { get; set; }

        /// <summary>
        /// UTC time message was sent
        /// </summary>
        [JsonProperty("timestamp"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime UtcTimeReceived { get; set; }
    }
}
