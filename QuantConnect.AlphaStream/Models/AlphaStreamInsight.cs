using System;
using System.ComponentModel;
using Newtonsoft.Json;
using QuantConnect.Algorithm.Framework.Alphas;
using QuantConnect.Algorithm.Framework.Alphas.Serialization;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Individual prediction from an Alpha.
    /// </summary>
    [JsonConverter(typeof(AlphaStreamInsightJsonConverter))]
    public class AlphaStreamInsight : Insight
    {
        /// <summary>
        /// Enum indicating the Insight creation moment.
        /// </summary>
        [JsonProperty("source")]
        public Source Source { get; private set; }

        public AlphaStreamInsight() : base(Symbol.Empty, TimeSpan.Zero, InsightType.Price, InsightDirection.Flat)
        {
        }

        public AlphaStreamInsight(DateTime generatedTimeUtc, Symbol symbol, TimeSpan period, InsightType type, InsightDirection direction,
            double? magnitude, double? confidence, string sourceModel = null, double? weight = null) :
            base(generatedTimeUtc, symbol, period, type, direction, magnitude, confidence, sourceModel, weight)
        {
        }

        /// <summary>
        /// Creates a new <see cref="AlphaStreamInsight"/> object from the specified serialized form
        /// </summary>
        /// <param name="serializedInsight">The insight DTO</param>
        /// <returns>A new insight containing the information specified</returns>
        public static AlphaStreamInsight FromSerializedAlphaStreamInsight(SerializedAlphaStreamInsight serializedInsight)
        {
            var insight = FromSerializedInsight(serializedInsight);

            return new AlphaStreamInsight(
                insight.GeneratedTimeUtc,
                insight.Symbol,
                insight.Period,
                insight.Type,
                insight.Direction,
                insight.Magnitude,
                insight.Confidence,
                insight.SourceModel,
                insight.Weight
            )
            {
                Id = insight.Id,
                CloseTimeUtc = insight.CloseTimeUtc,
                EstimatedValue = insight.EstimatedValue,
                ReferenceValue = insight.ReferenceValue,
                ReferenceValueFinal = insight.ReferenceValueFinal,
                GroupId = insight.GroupId,
                Score = insight.Score,
                Source = serializedInsight.Source
            };
        }
    }
}