using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Insight or Order source: in sample, out of sample, live trading.
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter), true)]
    public enum Source
    {
        /// <summary>
        /// Generated from backtesting across historical data.
        /// </summary>
        [EnumMember(Value = "in sample")] InSample,

        /// <summary>
        /// Generated from running a backtest on out of sample data.
        /// </summary>
        [EnumMember(Value = "out of sample")] OutOfSample,

        /// <summary>
        /// Generated from forward trading environment recorded at the moment they were generated
        /// </summary>
        [EnumMember(Value = "live trading")] LiveTrading,

        /// <summary>
        /// Unknown source
        /// </summary>
        [EnumMember(Value = "")] Unknown,
    }
}