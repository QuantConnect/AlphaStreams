using System;
using Newtonsoft.Json;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Individual prediction from an Alpha.
    /// </summary>
    public class Insight
    {
        /// <summary>
        /// Unique id of the Insight
        /// </summary>
        [JsonProperty("id")]
        public string Id { get; set; }

        /// <summary>
        /// Group id the Insight belongs to, null if not in a group
        /// </summary>
        [JsonProperty("group-id")]
        public string GroupId { get; set; }

        /// <summary>
        /// Alpha model that generated this Insight
        /// </summary>
        [JsonProperty("source-model")]
        public string SourceModel { get; set; }

        /// <summary>
        /// Confidence of the prediction as a percentage.
        /// </summary>
        [JsonProperty("confidence")]
        public double? Confidence { get; set; }

        /// <summary>
        /// Magnitude of the prediction
        /// </summary>
        [JsonProperty("magnitude")]
        public double? Magnitude { get; set; }

        /// <summary>
        /// Unix timestamp for the Alpha prediction.
        /// </summary>
        [JsonProperty("generated-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime Created { get; set; }

        /// <summary>
        /// Direction of the prediction, up or down.
        /// </summary>
        [JsonProperty("direction")]
        public Direction Direction { get; set; }

        /// <summary>
        /// Insight prediction source, in sample, out of sample, live trading.
        /// </summary>
        [JsonProperty("source")]
        public InsightSource Source { get; set; }

        /// <summary>
        /// Insight prediction type category, price or volatility.
        /// </summary>
        [JsonProperty("type")]
        public InsightType Type { get; set; }

        /// <summary>
        /// Reference value for this insight. Typically this is the raw asset price.
        /// </summary>
        [JsonProperty("reference")]
        public decimal? Reference { get; set; }

        /// <summary>
        /// The QuantConnect unique security identifier string for the asset
        /// </summary>
        [JsonProperty("symbol")]
        public string SymbolId { get; set; }

        /// <summary>
        /// Current ticker for this asset.
        /// </summary>
        [JsonProperty("ticker")]
        public string Ticker { get; set; }

        /// <summary>
        /// Timespan of the prediction in seconds.
        /// </summary>
        [JsonProperty("period")]
        public double? Period { get; set; }

        /// <summary>
        /// Estiated value of the insight
        /// </summary>
        [JsonProperty("estimated-value")]
        public double? EstimatedValue { get; set; }
    }
}