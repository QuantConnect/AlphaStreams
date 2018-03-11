using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Asset classes
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter), true)]
    public enum AssetClass
    {
        /// <summary>
        /// Unknown asset class
        /// </summary>
        [EnumMember(Value = "")] Unknown,

        /// <summary>
        /// Equity asset
        /// </summary>
        [EnumMember(Value = "equity")] Equity,

        /// <summary>
        /// Forex asset
        /// </summary>
        [EnumMember(Value = "forex")] Forex,

        /// <summary>
        /// Futures asset
        /// </summary>
        [EnumMember(Value = "future")] Future,

        /// <summary>
        /// Option asset
        /// </summary>
        [EnumMember(Value = "option")] Option,

        /// <summary>
        /// CFD asset
        /// </summary>
        [EnumMember(Value = "cfd")] Cfd,

        /// <summary>
        /// Cryptocurrency asset
        /// </summary>
        [EnumMember(Value = "crypto")] Crypto
    }
}