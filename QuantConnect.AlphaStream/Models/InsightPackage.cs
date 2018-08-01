using Newtonsoft.Json;
using System.Collections.Generic;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Wrapper packet to hold collection of Insight objects
    /// </summary>
    public class InsightPackage
    {
        /// <summary>
        /// Unique Alpha Id which generated this Insight
        /// </summary>
        [JsonProperty("alpha-id")]
        public string AlphaId { get; set; }

        /// <summary>
        /// Deploy id for this algorithm
        /// </summary>
        [JsonProperty("algorithm-id")]
        public string AlgorithmId { get; set; }

        /// <summary>
        /// Array of insights emitted at this timestep.
        /// </summary>
        [JsonProperty("insights")]
        public List<Insight> Insights { get; set; } = new List<Insight>();
    }
}