using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Direction of the insight; flat, up or down.
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter), true)]
    public enum Direction
    {
        /// <summary>
        /// Insight type (price/volatility) value will not move
        /// </summary>
        [EnumMember(Value = "flat")] Flat = 0,

        /// <summary>
        /// Insight type (price/volatility) value will move down
        /// </summary>
        [EnumMember(Value = "down")] Down = -1,

        /// <summary>
        /// Insight type (price/volatility) value will move up
        /// </summary>
        [EnumMember(Value = "up")] Up = 1
    }
}