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
            var stringBuilder = new StringBuilder($"{Id}: Location: {Location} Language: {Language} Alphas listed: {AlphasListed}");
            stringBuilder.Append($" Projects: {Projects} Backtests: {Backtests} Analysis average length: {AnalysisAverageLength}");

            if (Alphas.Count > 0)
            {
                stringBuilder.Append($" Alphas: {string.Join(", ", Alphas)}");
            }

            if (!extended)
            {
                return stringBuilder.ToString();
            }

            stringBuilder.Append($" Biography: {Biography.Substring(0, 50)}... Signup time: {SignupTime}");

            if (LastOnlineTime.HasValue)
            {
                stringBuilder.Append($" Last time online: {LastOnlineTime}");
            }

            if (ForumDiscussions > 0)
            {
                stringBuilder.Append($" ForumDiscussions: {ForumDiscussions}");
            }

            if (ForumComments > 0)
            {
                stringBuilder.Append($" Forum comments: {ForumComments}");
            }

            return stringBuilder.ToString();
        }

        /// <summary>
        /// Returns a string that represents the Author object
        /// </summary>
        /// <returns>A string that represents the Author object</returns>
        public override string ToString() => ToString(true);
    }
}