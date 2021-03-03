using System;
using Newtonsoft.Json;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Specifies a date range to search
    /// </summary>
    public class DateRange<T>
        where T : struct
    {
        /// <summary>
        /// Lower bound of the search criteria.
        /// </summary>
        [JsonProperty("minimum", DefaultValueHandling = DefaultValueHandling.Ignore)]
        [JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime? Minimum { get; set; }

        /// <summary>
        /// pper bound of the search criteria.
        /// </summary>
        [JsonProperty("maximum", DefaultValueHandling = DefaultValueHandling.Ignore)]
        [JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime? Maximum { get; set; }

        /// <summary>
        /// Initializes a new instance of the <see cref="DateRange{T}"/> class
        /// </summary>
        public DateRange()
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="DateRange{T}"/> class
        /// </summary>
        /// <param name="minimum">The minimum value</param>
        /// <param name="maximum">The maximum value</param>
        public DateRange(DateTime? minimum, DateTime? maximum)
        {
            Minimum = minimum;
            Maximum = maximum;
        }
    }
}