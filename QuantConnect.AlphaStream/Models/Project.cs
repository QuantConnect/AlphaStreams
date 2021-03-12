using System;
using Newtonsoft.Json;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Project object where the Alpha source resides. One Project can have multiple generated Alphas.
    /// </summary>
    public class Project
    {
        /// <summary>
        /// Alpha project author.
        /// </summary>
        [JsonProperty("author")]
        public Author Author { get; set; }

        /// <summary>
        /// Author assigned project name.
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Unix timestamp when the project was created.
        /// </summary>
        [JsonProperty("created-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime CreatedTime { get; set; }

        /// <summary>
        /// Unix timestamp last time the project was opened/modified.
        /// </summary>
        [JsonProperty("last-modified-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime LastModifiedTime { get; set; }

        /// <summary>
        /// Returns a string that represents the Project object
        /// </summary>
        /// <returns>A string that represents the Project object</returns>
        public override string ToString()
        {
            return $"{Name} Created Time: {CreatedTime} Last time modified: {LastModifiedTime} Author: {Author}";
        }
    }
}