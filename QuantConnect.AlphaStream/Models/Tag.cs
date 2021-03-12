using Newtonsoft.Json;

namespace QuantConnect.AlphaStream.Models
{
    public class Tag
    {
        [JsonProperty("matches")]
        public int Matches { get; set; }

        [JsonProperty("tag")]
        public string TagName { get; set; }

        /// <summary>
        /// Returns a string that represents the Tag object
        /// </summary>
        /// <returns>A string that represents the Tag object</returns>
        public override string ToString()
        {
            return $"{TagName} has {Matches} matches";
        }
    }
}