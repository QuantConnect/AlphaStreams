using Newtonsoft.Json;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Result of a bid to license an Alpha
    /// </summary>
    public class Bid
    {
        /// <summary>
        /// Capacity allocated if the bid is successful
        /// </summary>
        [JsonProperty("id")]
        public int Id { get; set; }

        /// <summary>
        /// True if the bid resulted in a new license
        /// </summary>
        [JsonProperty("auto-renew")]
        public bool AutoRenew { get; set; }

        /// <summary>
        /// True if the bid resulted in a new license
        /// </summary>
        [JsonProperty("good-until-time")]
        public decimal GoodUntil { get; set; }

        /// <summary>
        /// True if the bid resulted in a new license
        /// </summary>
        [JsonProperty("allocation")]
        public decimal Allocation { get; set; }

        /// <summary>
        /// True if the bid resulted in a new license
        /// </summary>
        [JsonProperty("license-period")]
        public decimal LicensePeriod { get; set; }

        /// <summary>
        /// True if the bid resulted in a new license
        /// </summary>
        [JsonProperty("maximum-price")]
        public decimal MaximumPrice { get; set; }
    }
}