using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Insight prediction type category, price or volatility.
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter), true)]
    public enum InsightType
    {
        /// <summary>
        /// Predicting a change in price
        /// </summary>
        [EnumMember(Value = "price")] Price,

        /// <summary>
        /// Predicting a change in volatility
        /// </summary>
        [EnumMember(Value = "volatility")] Volatility
    }
}