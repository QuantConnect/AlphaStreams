using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using QuantConnect.Orders;
using QuantConnect.Orders.Serialization;

namespace QuantConnect.AlphaStream.Models.Orders
{
    public class AlphaStreamOrder : SerializedOrder
    {
        /// <summary>
        /// Specifies the source of this order, live trading/backtesting/out of sample
        /// </summary>
        [JsonProperty("source")]
        public Source Source { get; set; } = Source.Unknown;

        /// <summary>
        /// The orders <see cref="AlphaStreamOrderEvent"/>
        /// </summary>
        [JsonProperty("events")]
        public List<AlphaStreamOrderEvent> OrderEvents { get; set; } = new List<AlphaStreamOrderEvent>();

        /// <summary>
        /// Creates a new serialized order instance based on the provided order
        /// </summary>
        public AlphaStreamOrder()
        {
        }

        /// <summary>
        /// Creates a new serialized order instance based on the provided order
        /// </summary>
        public AlphaStreamOrder(Order order, string algorithmId) : base(order, algorithmId)
        {
        }

        /// <summary>
        /// Returns a string that represents the current object.
        /// </summary>
        public override string ToString()
        {
            var stringBuilder = new StringBuilder();

            stringBuilder.Append($"ID: {Id} Source '{Source}' Symbol: {Symbol} Status: {Status} CreatedTime: {CreatedTime} Direction {Direction} Quantity {Quantity} Type: {Type} TimeInForceType: {TimeInForceType}");

            if (TimeInForceExpiry.HasValue)
            {
                stringBuilder.Append($" TimeInForceExpiry: {TimeInForceExpiry}");
            }

            if (BrokerId.Count > 0)
            {
                stringBuilder.Append($" BrokerId: [{string.Join(",", BrokerId)}]");
            }

            if (Price != 0)
            {
                stringBuilder.Append($" Price: {Price} {PriceCurrency}");
            }

            if (ContingentId != 0)
            {
                stringBuilder.Append($" ContingentId: {ContingentId}");
            }

            if (LastUpdateTime.HasValue)
            {
                stringBuilder.Append($" LastUpdateTime: {LastUpdateTime}");
            }
            if (LastFillTime.HasValue)
            {
                stringBuilder.Append($" LastFillTime: {LastFillTime}");
            }
            if (CanceledTime.HasValue)
            {
                stringBuilder.Append($" CanceledTime: {CanceledTime}");
            }

            if (LimitPrice.HasValue)
            {
                stringBuilder.Append($" LimitPrice: {LimitPrice.Value}");
            }
            if (StopPrice.HasValue)
            {
                stringBuilder.Append($" StopPrice: {StopPrice.Value}");
            }

            if (SubmissionLastPrice != 0)
            {
                stringBuilder.Append($" SubmissionLastPrice: {SubmissionLastPrice}");
            }
            if (SubmissionAskPrice != 0)
            {
                stringBuilder.Append($" SubmissionAskPrice: {SubmissionAskPrice}");
            }
            if (SubmissionBidPrice != 0)
            {
                stringBuilder.Append($" SubmissionBidPrice: {SubmissionBidPrice}");
            }

            if (!string.IsNullOrEmpty(Tag))
            {
                stringBuilder.Append($" Tag: '{Tag}'");
            }

            if (OrderEvents.Count > 0)
            {
                stringBuilder.Append(" OrderEvents: [{");
                stringBuilder.Append(string.Join("},{", OrderEvents.Select(orderEvent => orderEvent.ToString(false))));
                stringBuilder.Append("}]");
            }

            return stringBuilder.ToString();
        }
    }
}
