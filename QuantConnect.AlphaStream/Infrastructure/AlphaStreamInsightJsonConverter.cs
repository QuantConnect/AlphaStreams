using Newtonsoft.Json;
using QuantConnect.Algorithm.Framework.Alphas;
using QuantConnect.Algorithm.Framework.Alphas.Serialization;
using QuantConnect.AlphaStream.Models;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Defines how insights should be serialized to json
    /// </summary>
    public class AlphaStreamInsightJsonConverter : TypeChangeJsonConverter<AlphaStreamInsight, SerializedAlphaStreamInsight>
    {
        /// <summary>
        /// Convert the input value to a value to be serialized
        /// </summary>
        /// <param name="value">The input value to be converted before serialization</param>
        /// <returns>A new instance of TResult that is to be serialized</returns>
        protected override SerializedAlphaStreamInsight Convert(AlphaStreamInsight value)
        {
            return new SerializedAlphaStreamInsight(value);
        }

        /// <summary>
        /// Converts the input value to be deserialized
        /// </summary>
        /// <param name="value">The deserialized value that needs to be converted to T</param>
        /// <returns>The converted value</returns>
        protected override AlphaStreamInsight Convert(SerializedAlphaStreamInsight value)
        {
            return AlphaStreamInsight.FromSerializedAlphaStreamInsight(value);
        }
    }

    public class SerializedAlphaStreamInsight : SerializedInsight
    {
        /// <summary>
        /// Enum indicating the Insight creation moment.
        /// </summary>
        [JsonProperty("source")]
        public Source Source { get; }

        /// <summary>
        /// Initializes a new default instance of the <see cref="SerializedInsight"/> class
        /// </summary>
        public SerializedAlphaStreamInsight()
        {
        }

        public SerializedAlphaStreamInsight(AlphaStreamInsight insight) : base(insight)
        {
            Source = insight.Source;
        }
    }
}