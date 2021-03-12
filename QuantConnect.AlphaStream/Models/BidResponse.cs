using Newtonsoft.Json;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Result of a bid to license an Alpha
    /// </summary>
    public class BidResponse : ApiResponse
    {
        /// <summary>
        /// Capacity allocated if the bid is successful
        /// </summary>
        [JsonProperty("capacity-allocated")]
        public decimal CapacityAllocated { get; set; }

        /// <summary>
        /// True if the bid resulted in a new license
        /// </summary>
        [JsonProperty("licensed")]
        public bool Licensed { get; set; }

        /// <summary>
        /// True if the out bid
        /// </summary>
        [JsonProperty("Outbid")]
        public bool Outbid { get; set; }

        /// <summary>
        /// Returns a string that represents the BidResponse object
        /// </summary>
        /// <returns>A string that represents the BidResponse object</returns>
        public override string ToString()
        {
            if (!Success)
            {
                return base.ToString();
            }

            if (Licensed)
            {
                return $"Congratulations! Your bid on the alpha was successful and your license with a ${CapacityAllocated} allocation for the alphas has started.";
            }

            if (Outbid)
            {
                return "Your bid for shares was recently outbid and we believe you may not win the final auction.";
            }

            return "Not licensed nor outbid. Please contact support@quantconnect.com";
        }
    }
}