using System;
using Newtonsoft.Json;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Models
{
    public class EquityCurve
    {
        /// <summary>
        /// Timestamp of equity curve point
        /// </summary>
        [JsonProperty("time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime Time { get; set; }

        /// <summary>
        /// Dollar value of the equity
        /// </summary>
        [JsonProperty("equity")]
        public double Equity { get; set; }

        /// <summary>
        /// Sample of equity point (in-sample or live-trading)
        /// </summary>
        [JsonProperty("sample")]
        public string Sample { get; set; }

        /// <summary>
        /// Returns a string that represents the EquityCurve object
        /// </summary>
        /// <returns>A string that represents the EquityCurve object</returns>
        public override string ToString()
        {
            return $"{Time},{Equity},{Sample}";
        }
    }
}