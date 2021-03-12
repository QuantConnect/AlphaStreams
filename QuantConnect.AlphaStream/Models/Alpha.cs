using System;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Linq;
using System.Text;

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
        public List<SecurityType> AssetClasses { get; set; } = new List<SecurityType>();

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

        /// <summary>
        /// Alpha's capacity: the maximum funds that can be allocated to it
        /// </summary>
        [JsonProperty("capacity")]
        public decimal? Capacity { get; set; }

        /// <summary>
        /// Alpha's allocated capacity: funds allocated so far
        /// </summary>
        [JsonProperty("capacity-allocated")]
        public decimal? CapacityAllocated { get; set; }

        /// <summary>
        /// Alpha's reserve price
        /// </summary>
        [JsonProperty("reserve-price")]
        public decimal? ReservePrice { get; set; }

        /// <summary>
        /// Returns a string that represents the Alpha object
        /// </summary>
        /// <param name="extended">False if we want the short version</param>
        /// <returns>A string that represents the Alpha object</returns>
        public string ToString(bool extended)
        {
            var stringBuilder = new StringBuilder($"{Id}\t'{Name} v{Version}'{Environment.NewLine}Status:\t{Status}");

            if (AssetClasses.Count > 0)
            {
                stringBuilder.Append($"{Environment.NewLine}Asset Classes:\t{string.Join(", ", AssetClasses)}");
            }

            if (Tags.Count > 0)
            {
                stringBuilder.Append($"{Environment.NewLine}Tags:\t{string.Join(", ", Tags)}");
            }

            if (SharpeRatio.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Sharpe Ratio:\t{SharpeRatio.Value}");
            }

            if (Uniqueness.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Uniqueness:\t{Uniqueness.Value}");
            }

            if (Accuracy.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Accuracy:\t{Accuracy.Value}");
            }

            if (ReturnsCorrelation.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Returns correlation:\t{ReturnsCorrelation.Value}");
            }

            if (DtwDistance.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Dynamic Time Wrap:\t{DtwDistance.Value}");
            }

            if (Capacity.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Capacity:\t{Capacity.Value}");
            }

            if (CapacityAllocated.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Allocated capacity:\t{CapacityAllocated.Value}");
            }

            if (ReservePrice.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Reserve price:\t{ReservePrice.Value}");
            }

            if (!extended)
            {
                return stringBuilder.ToString();
            }

            stringBuilder.Append($"{Environment.NewLine}Description:\t{Description.Substring(0, 100)}...");
            stringBuilder.Append($"{Environment.NewLine}Project:\t{Project}");

            if (Authors.Count > 0)
            {
                stringBuilder.Append($"{Environment.NewLine}Authors:\t{Authors.Count}");
                stringBuilder.Append($"{Environment.NewLine}{string.Join(", ", Authors.Select(a => a.ToString()))}");
            }

            if (AuthorTrading.HasValue && AuthorTrading.Value)
            {
                stringBuilder.Append($"{Environment.NewLine}Author is trading");
            }

            if (AnalysesPerformed.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Analyses performed:\t{AnalysesPerformed.Value}");
            }

            if (EstimatedEffort.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Estimated effort:\t{EstimatedEffort.Value}");
            }

            if (EstimatedDepth.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Estimated depth:\t{EstimatedDepth.Value}");
            }

            if (Parameters > 0)
            {
                stringBuilder.Append($"{Environment.NewLine}Parameters:\t{Parameters.Value}");
            }

            if (InSampleInsights.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}In sample insights:\t{InSampleInsights.Value}");
            }

            if (OutOfSampleInsights.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Out of sample insights:\t{OutOfSampleInsights.Value}");
            }

            if (LiveTradingInsights.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Live trading insights:\t{LiveTradingInsights.Value}");
            }

            if (Trial > 0)
            {
                stringBuilder.Append($"{Environment.NewLine}Trial period:\t{Trial.Value}");
            }

            return stringBuilder.ToString();
        }

        /// <summary>
        /// Returns a string that represents the Alpha object
        /// </summary>
        /// <returns>A string that represents the Alpha object</returns>
        public override string ToString() => ToString(true);

        /// <summary>
        /// Returns a string that represents the Alpha object
        /// </summary>
        /// <param name="extended">False if we want the short version</param>
        /// <returns>A string that represents the Alpha object</returns>
        public string ToStringInline(bool extended = false) => ToString(extended).Replace(Environment.NewLine, " ");
    }
}