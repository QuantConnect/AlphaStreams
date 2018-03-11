using Newtonsoft.Json;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// A time-value pair
    /// </summary>
    public class Point
    {
        /// <summary>
        /// Time value of a time-value pair.
        /// </summary>
        [JsonProperty("time")]
        public long Time { get; set; }

        /// <summary>
        /// Value of the point.
        /// </summary>
        [JsonProperty("value")]
        public double Value { get; set; }
    }
}