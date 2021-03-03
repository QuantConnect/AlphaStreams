using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using QuantConnect.Util;

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
    }
}