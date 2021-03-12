using Newtonsoft.Json;
using QuantConnect.Util;
using System;
using System.Collections.Generic;
using System.Text;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Author user of QuantConnect responsible for creation of an Alpha.
    /// </summary>
    public class Author
    {
        /// <summary>
        /// Unique string hash id for Author.
        /// </summary>
        [JsonProperty("id")]
        public string Id { get; set; }

        /// <summary>
        /// String array of Alpha-Id hashes the Author has created.
        /// </summary>
        [JsonProperty("alphas")]
        public List<string> Alphas { get; set; } = new List<string>();

        /// <summary>
        /// Number of Alphas Author has listed in the marketplace.
        /// </summary>
        [JsonProperty("alphas-listed")]
        public int AlphasListed { get; set; }

        /// <summary>
        /// Number of days of the average analysis(backtest) length for the Author.
        /// </summary>
        [JsonProperty("analysis-average-length")]
        public int? AnalysisAverageLength { get; set; }

        /// <summary>
        /// Lifetime number of analysis(backtests) conducted by the Author.
        /// </summary>
        [JsonProperty("backtests")]
        public int Backtests { get; set; }

        /// <summary>
        /// Profile auto-biography (100-500 words).
        /// </summary>
        [JsonProperty("biography")]
        public string Biography { get; set; }

        /// <summary>
        /// Number of forum discussions started by the Author.
        /// </summary>
        [JsonProperty("forum-discussions")]
        public int ForumDiscussions { get; set; }

        /// <summary>
        /// Number of forum comments made by the Author.
        /// </summary>
        [JsonProperty("forum-comments")]
        public int ForumComments { get; set; }

        /// <summary>
        /// Researcher preferred programming language.
        /// </summary>
        [JsonProperty("language")]
        public Language Language { get; set; }

        /// <summary>
        /// Unix timestamp of the last time the Author was online (Updated daily).
        /// </summary>
        [JsonProperty("last-online-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime? LastOnlineTime { get; set; }

        /// <summary>
        /// Best known estimate of the Author geographic location.
        /// </summary>
        [JsonProperty("location")]
        public string Location { get; set; }

        /// <summary>
        /// Total count of the number of projects the Author has in account.
        /// </summary>
        [JsonProperty("projects")]
        public int Projects { get; set; }

        /// <summary>
        /// Unix timestamp of the user sign up.
        /// </summary>
        [JsonProperty("signup-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime SignupTime { get; set; }

        /// <summary>
        /// Array of social media profile links.
        /// </summary>
        [JsonProperty("social-media")]
        public List<string> SocialMedia { get; set; } = new List<string>();

        /// <summary>
        /// Returns a string that represents the Author object
        /// </summary>
        /// <param name="extended">False if we want the short version</param>
        /// <returns>A string that represents the Author object</returns>
        public string ToString(bool extended)
        {
            var stringBuilder = new StringBuilder($"Author Id:\t{Id}");

            if (Alphas.Count > 0)
            {
                stringBuilder.Append($"{Environment.NewLine}Alphas listed:\t{AlphasListed}");
                stringBuilder.Append($"{Environment.NewLine}Alphas:\t{string.Join(", ", Alphas)}");
            }

            stringBuilder.Append($"{Environment.NewLine}Location:\t{Location}");
            stringBuilder.Append($"{Environment.NewLine}Language:\t{Language}");
            stringBuilder.Append($"{Environment.NewLine}Projects:\t{Projects}");
            stringBuilder.Append($"{Environment.NewLine}Backtests:\t{Backtests}");
            stringBuilder.Append($"{Environment.NewLine}Analysis average length:\t{AnalysisAverageLength}");

            if (!extended)
            {
                return stringBuilder.ToString();
            }

            stringBuilder.Append($"{Environment.NewLine}Biography:\t{Biography.Substring(0, 100)}...");
            stringBuilder.Append($"{Environment.NewLine}Sign-up time:\t{SignupTime}");

            if (LastOnlineTime.HasValue)
            {
                stringBuilder.Append($"{Environment.NewLine}Last time online:\t{LastOnlineTime}");
            }

            if (ForumDiscussions > 0)
            {
                stringBuilder.Append($"{Environment.NewLine}Forum discussions:\t{ForumDiscussions}");
            }

            if (ForumComments > 0)
            {
                stringBuilder.Append($"{Environment.NewLine}Forum comments:\t{ForumComments}");
            }

            return stringBuilder.ToString();
        }

        /// <summary>
        /// Returns a string that represents the Author object
        /// </summary>
        /// <returns>A string that represents the Author object</returns>
        public override string ToString() => ToString(true);

        /// <summary>
        /// Returns a string that represents the Author object
        /// </summary>
        /// <param name="extended">False if we want the short version</param>
        /// <returns>A string that represents the Author object</returns>
        public string ToStringInline(bool extended = false) => ToString(extended).Replace(Environment.NewLine, " ");
    }
}