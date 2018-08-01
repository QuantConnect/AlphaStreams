using Newtonsoft.Json;
using QuantConnect.AlphaStream.Infrastructure;
using System;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Record of the price of an Alpha or a bid made for it.
    /// </summary>
    public class Price
    {
        /// <summary>
        /// Unix timestamp of the last time the price was updated.
        /// </summary>
        [JsonProperty("time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime Time { get; set; }

        /// <summary>
        /// The type of price update. Can be bid, ask or trade. Only ask supported at this time.
        /// </summary>
        [JsonProperty("price-type")]
        public PriceType PriceType { get; set; } = PriceType.Ask;

        /// <summary>
        /// Shared price for this moment of time.
        /// </summary>
        [JsonProperty("shared-price")]
        public decimal? SharedPrice { get; set; }

        /// <summary>
        /// Exclusive price for this moment of time.
        /// </summary>
        [JsonProperty("exclusive-price")]
        public decimal? ExclusivePrice { get; set; }
    }
}