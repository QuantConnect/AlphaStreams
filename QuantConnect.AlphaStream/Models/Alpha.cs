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
        /// Unique hash identifier for this published Alpha.
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
        /// Daily rolling accuracy of the Alpha module over the last 30 days of insight direction score.
        /// </summary>
        [JsonProperty("accuracy")]
        public double? Accuracy { get; set; }

        /// <summary>
        /// Number of backtests/analysis trials used to generate this Alpha model.
        /// </summary>
        [JsonProperty("analyses-performed")]
        public int? AnalysesPerformed { get; set; }

        /// <summary>
        /// Boolean indicating whether the author is actively trading this alpha on their own account
        /// </summary>
        [JsonProperty("author-trading")]
        public bool? AuthorTrading { get; set; }

        /// <summary>
        /// Author supplied paragraph description of the Alpha behavior
        /// </summary>
        [JsonProperty("description")]
        public string Description { get; set; }

        /// <summary>
        /// Name of the Alpha as listed in the marketplace
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

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
        /// Sharpe ratio of the Alpha with a $1M portfolio, equal weighting portfolio construction and immediate execution models. NOTE: This is currently not implemented.
        /// </summary>
        [JsonProperty("sharpe-ratio")]
        public double? SharpeRatio { get; set; }

        /// <summary>
        /// Monthly fee levied by the author on the Alpha signal.
        /// </summary>
        [JsonProperty("subscription-fee")]
        public decimal? SubscriptionFee { get; set; }

        /// <summary>
        /// Alphas are forced-running by default but after 10 production runtime errors they are taken offline.
        /// </summary>
        [JsonProperty("status")]
        public AlphaStatus Status { get; set; }

        /// <summary>
        /// Version of the Alpha. Number of times this Project has been listed into the marketplace.
        /// </summary>
        [JsonProperty("version")]
        public string Version { get; set; }

        /// <summary>
        /// Alpha Tags. Tag the alpha with some custom data
        /// </summary>
        [JsonProperty("tags")]
        public List<string> Tags { get; set; } = new List<string>();

        /// <summary>
        /// Represents the number of parameters that the alpha uses.
        /// If the alpha has not been reviewed for parameters this value is null.
        /// </summary>
        [JsonProperty("parameters")]
        public int? Parameters { get; set; } = null;

        /// <summary>
        /// Number of in-sample Insights
        /// </summary>
        [JsonProperty("in-sample-insights")]
        public int? InSampleInsights { get; set; }

        /// <summary>
        /// Number of live-trading Insights
        /// </summary>
        [JsonProperty("live-trading-insights")]
        public int? LiveTradingInsights { get; set; }

        /// <summary>
        /// Number of out-of-sample Insights
        /// </summary>
        [JsonProperty("out-of-sample-insights")]
        public int? OutOfSampleInsights { get; set; }

        /// <summary>
        /// Out of sample DTW distance
        /// </summary>
        [JsonProperty("out-of-sample-dtw-distance")]
        public double? DtwDistance { get; set; }

        /// <summary>
        /// Out of sample returns correlation
        /// </summary>
        [JsonProperty("out-of-sample-returns-correlation")]
        public double? ReturnsCorrelation { get; set; }

        /// <summary>
        /// Alpha's trial period
        /// </summary>
        [JsonProperty("trial")]
        public int? Trial { get; set; } = 0;
    }
}