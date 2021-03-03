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
        /// Insights generated from backtesting across historical data.
        /// </summary>
        [EnumMember(Value = "in sample")] InSample,

        /// <summary>
        /// Insights from running a backtest on out of sample data.
        /// </summary>
        [EnumMember(Value = "out of sample")] OutOfSample,

        /// <summary>
        /// Insights from forward trading environment recorded at the moment they were generated
        /// </summary>
        [EnumMember(Value = "live trading")] LiveTrading
    }
}