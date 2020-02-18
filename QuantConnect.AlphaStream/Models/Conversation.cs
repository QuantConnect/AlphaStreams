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
        /// Hash id of the sender
        /// </summary>
        [JsonProperty("from")]
        public Dictionary<string, string> From { get; set; }

        /// <summary>
        /// UTC time message was sent
        /// </summary>
        [JsonProperty("timestamp"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime TimeReceived { get; set; }
    }
}
