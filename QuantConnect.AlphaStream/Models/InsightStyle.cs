using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Predictions are discrete (binary up-down) or a specific value prediction.
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter), true)]
    public enum InsightStyle
    {
        /// <summary>
        /// Specific value prediction
        /// </summary>
        [EnumMember(Value = "continuous")] Continuous,

        /// <summary>
        /// Directional prediction
        /// </summary>
        [EnumMember(Value = "discrete")] Discrete
    }
}