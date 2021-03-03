using Newtonsoft.Json;
using System;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Individual error set for an Alpha in the QuantConnect Alpha Streams market
    /// </summary>
    public class RuntimeError
    {
        /// <summary>
        /// The unix timestamp of the production runtime error.
        /// </summary>
        [JsonProperty("time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime Time { get; set; }

        /// <summary>
        /// Error message string from the Alpha.
        /// </summary>
        [JsonProperty("error")]
        public string Error { get; set; }

        /// <summary>
        /// Stacktrace of the production error recorded from the Alpha.
        /// </summary>
        [JsonProperty("stacktrace")]
        public string StackTrace { get; set; }
    }
}