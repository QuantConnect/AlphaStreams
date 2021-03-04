using System;
using Newtonsoft.Json;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Information on a specific bid made to license an Alpha
    /// </summary>
    public class Bid
    {
        /// <summary>
        /// Unique ID of the Bid
        /// </summary>
        [JsonProperty("id")]
        public int Id { get; set; }

        /// <summary>
        /// True if the bid will be automatically renewed when the license expires
        /// </summary>
        [JsonProperty("auto-renew")]
        public bool AutoRenew { get; set; }

        /// <summary>
        /// Expiration time of the bid.
        /// </summary>
        [JsonProperty("good-until-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime GoodUntil { get; set; }

        /// <summary>
        /// Allocation that the alpha will be licensed to
        /// </summary>
        [JsonProperty("allocation")]
        public decimal Allocation { get; set; }

        /// <summary>
        /// Period that the alpha will be licensed to (in days)
        /// </summary>
        [JsonProperty("license-period")]
        public decimal LicensePeriod { get; set; }

        /// <summary>
        /// The maximum bid price per 4-week period
        /// </summary>
        [JsonProperty("maximum-price")]
        public decimal MaximumPrice { get; set; }
    }
}