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
        /// Unique hash id of this Insight
        /// </summary>
        [JsonProperty("id")]
        public string Id { get; set; }

        /// <summary>
        /// Insight prediction type category: price or volatility.
        /// </summary>
        [JsonProperty("type")]
        public InsightType Type { get; set; }

        /// <summary>
        /// Direction of the insight; flat, up or down.
        /// </summary>
        [JsonProperty("direction")]
        public Direction Direction { get; set; }

        /// <summary>
        /// Timespan of the prediction in seconds.
        /// </summary>
        [JsonProperty("period")]
        public double? Period { get; set; }

        /// <summary>
        /// Unix timestamp for when the Alpha Insight was created.
        /// </summary>
        [JsonProperty("created-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime CreatedTime { get; set; }

        /// <summary>
        /// Unix timestamp for when the Alpha Insight was closed (start + period).
        /// </summary>
        [JsonProperty("close-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime CloseTime { get; set; }

        /// <summary>
        /// Predicted percent change in the insight type (price/volatility)
        /// </summary>
        [JsonProperty("magnitude")]
        public double? Magnitude { get; set; }

        /// <summary>
        /// Confidence of the Insight as a percentage.
        /// </summary>
        [JsonProperty("confidence")]
        public double? Confidence { get; set; }

        /// <summary>
        /// Identifier for the source model that generated this insight.
        /// </summary>
        [JsonProperty("source-model")]
        public string SourceModel { get; set; }

        /// <summary>
        /// Group id this insight belongs to
        /// </summary>
        [JsonProperty("group")]
        public string Group { get; set; }

        /// <summary>
        /// Enum indicating the Insight creation moment.
        /// </summary>
        [JsonProperty("source")]
        public InsightSource Source { get; set; }

        /// <summary>
        /// Sample of the asset price at the time the insight was created
        /// </summary>
        [JsonProperty("reference-value")]
        public decimal? ReferenceValue { get; set; }

        /// <summary>
        /// Estimated value of this insight in the account currency
        /// </summary>
        [JsonProperty("estimated-value")]
        public decimal? EstimatedValue { get; set; }

        /// <summary>
        /// Uniquely identified securities-contract based on QuantConnect.Symbol type. All information to uniquely identify a contract.
        /// </summary>
        [JsonProperty("symbol")]
        public string SymbolId { get; set; }

        /// <summary>
        /// Current ticker for this asset
        /// </summary>
        [JsonProperty("ticker")]
        public string Ticker { get; set; }
    }
}