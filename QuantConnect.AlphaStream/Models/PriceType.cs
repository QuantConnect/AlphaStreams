using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Runtime.Serialization;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// The type of price update. Can be bid, ask or trade.
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter), true)]
    public enum PriceType
    {
        /// <summary>
        /// Unknown price type
        /// </summary>
        [EnumMember(Value = "")] Unknown,

        /// <summary>
        /// Ask price type
        /// </summary>
        [EnumMember(Value = "ask")] Ask,

        /// <summary>
        /// Bid price type
        /// </summary>
        [EnumMember(Value = "bid")] Bid,

        /// <summary>
        /// Trade price type
        /// </summary>
        [EnumMember(Value = "trade")] Trade
    }
}