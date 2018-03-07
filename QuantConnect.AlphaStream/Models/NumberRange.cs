using Newtonsoft.Json;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Specifies a numeric range of values to search
    /// </summary>
    public class NumberRange<T>
        where T : struct
    {
        /// <summary>
        /// Lower bound of the search criteria.
        /// </summary>
        [JsonProperty("minimum", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public T? Minimum { get; set; }

        /// <summary>
        /// pper bound of the search criteria.
        /// </summary>
        [JsonProperty("maximum", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public T? Maximum { get; set; }

        /// <summary>
        /// Initializes a new instance of the <see cref="DateRange{T}"/> class
        /// </summary>
        public NumberRange()
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="NumberRange{T}"/> class
        /// </summary>
        /// <param name="minimum">The minimum value</param>
        /// <param name="maximum">The maximum value</param>
        public NumberRange(T? minimum, T? maximum)
        {
            Minimum = minimum;
            Maximum = maximum;
        }
    }
}