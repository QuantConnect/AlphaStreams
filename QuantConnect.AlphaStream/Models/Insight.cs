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
        /// Confidence of the prediction as a percentage.
        /// </summary>
        [JsonProperty("confidence")]
        public double? Confidence { get; set; }

        /// <summary>
        /// Unix timestamp for the Alpha prediction.
        /// </summary>
        [JsonProperty("created"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime Created { get; set; }

        /// <summary>
        /// Direction of the prediction, up or down.
        /// </summary>
        [JsonProperty("direction")]
        public Direction Direction { get; set; }

        /// <summary>
        /// Predictions are discrete (binary up-down) or a specific value prediction.
        /// </summary>
        [JsonProperty("insight-style")]
        public InsightStyle InsightStyle { get; set; }

        /// <summary>
        /// Insight prediction source, in sample, out of sample, live trading.
        /// </summary>
        [JsonProperty("source")]
        public InsightSource InsightSource { get; set; }

        /// <summary>
        /// Insight prediction type category, price or volatility.
        /// </summary>
        [JsonProperty("insight-type")]
        public InsightType InsightType { get; set; }

        /// <summary>
        /// Flag the insight was generated live (created == now).
        /// </summary>
        [JsonProperty("live")]
        public bool Live { get; set; }

        /// <summary>
        /// Reference value for this insight
        /// </summary>
        [JsonProperty("reference")]
        public decimal? Reference { get; set; }

        /// <summary>
        /// The QuantConnect unique security identifier string for the asset
        /// </summary>
        [JsonProperty("symbol")]
        public string SymbolId { get; set; }

        /// <summary>
        /// Timespan of the prediction in seconds.
        /// </summary>
        [JsonProperty("timeframe")]
        public double Timeframe { get; set; }
    }
}