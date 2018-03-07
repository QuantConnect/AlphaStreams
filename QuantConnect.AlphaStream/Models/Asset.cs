using Newtonsoft.Json;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Individual Asset mentioned in an Insight prediction.
    /// </summary>
    public class Asset
    {
        /// <summary>
        /// The current price of the asset.
        /// </summary>
        [JsonProperty("price")]
        public decimal Price { get; set; }

        /// <summary>
        /// The assets ticket symbol
        /// </summary>
        [JsonProperty("symbol")]
        public string Symbol { get; set; }

        /// <summary>
        /// Average daily volume for asset in USD.
        /// </summary>
        [JsonProperty("volume")]
        public decimal Volume { get; set; }
    }
}