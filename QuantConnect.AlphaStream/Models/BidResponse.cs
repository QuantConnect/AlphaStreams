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
    }
}