using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Snapshot of a Project at the time it was deployed to the marketplace, written by an Author on QuantConnect, generating Insights about Assets.
    /// </summary>
    public class Alpha
    {
        /// <summary>
        /// Unique identifier for this published Alpha.
        /// </summary>
        [JsonProperty("id")]
        public string Id { get; set; }

        /// <summary>
        /// Creators of the Alpha. Sometimes users collaborate on a Project or have one trader paired with a coder. Authors can be added and removed from projects.
        /// </summary>
        [JsonProperty("authors")]
        public List<Author> Authors { get; set; } = new List<Author>();

        /// <summary>
        /// Asset classes predicted in this stream.
        /// </summary>
        [JsonProperty("asset-classes")]
        public List<AssetClass> AssetClasses { get; set; } = new List<AssetClass>();

        /// <summary>
        /// Daily rolling accuracy of the Alpha module over the last 7 days of predictions.
        /// </summary>
        [JsonProperty("accuracy")]
        public double Accuracy { get; set; }

        /// <summary>
        /// Number of backtests/analysis trials used to generate this Alpha model.
        /// </summary>
        [JsonProperty("analyses-performed")]
        public int? AnalysesPerformed { get; set; }

        /// <summary>
        /// Estimated market depth available for this asset based on trading volumes at the time of Insights.
        /// </summary>
        [JsonProperty("estimated-depth")]
        public double? EstimatedDepth { get; set; }

        /// <summary>
        /// Estimated number of hours the user was working on this Alpha.
        /// </summary>
        [JsonProperty("estimated-effort")]
        public double? EstimatedEffort { get; set; }

        /// <summary>
        /// Flag to indicate if the author is open to selling the signal exclusively.
        /// </summary>
        [JsonProperty("exclusive-available")]
        public bool? ExclusiveAvailable { get; set; }

        /// <summary>
        /// Monthly fee for exclusive access to the Alpha signal.
        /// </summary>
        [JsonProperty("exclusive-subscription-fee")]
        public decimal? ExclusiveSubscriptionFee { get; set; }

        /// <summary>
        /// Unix timestamp the Alpha was listed into the marketplace.
        /// </summary>
        [JsonProperty("listed-date"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime? ListedDate { get; set; }

        /// <summary>
        /// Project object where the Alpha source resides. One Project can have multiple generated Alphas.
        /// </summary>
        [JsonProperty("project")]
        public Project Project { get; set; }

        /// <summary>
        /// Indicator of uniqueness in in the QuantConnect marketplace based on the assets traded and the overlap of signal with other Alphas in the Client portfolio, where percentage of overlap with other Alphas (100% is identical).
        /// </summary>
        [JsonProperty("uniqueness")]
        public double? Uniqueness { get; set; }

        /// <summary>
        /// Sharpe ratio of the Alpha with QuantConnect default cumulative equity backtest applied.
        /// </summary>
        [JsonProperty("sharpe-ratio")]
        public double? SharpeRatio { get; set; }

        /// <summary>
        /// Monthly fee levied by the author on the Alpha signal.
        /// </summary>
        [JsonProperty("subscription-fee")]
        public decimal? SubscriptionFee { get; set; }

        /// <summary>
        /// Version of the Alpha. Number of times this Project has been listed into the marketplace.
        /// </summary>
        [JsonProperty("version")]
        public string Version { get; set; }
    }
}
