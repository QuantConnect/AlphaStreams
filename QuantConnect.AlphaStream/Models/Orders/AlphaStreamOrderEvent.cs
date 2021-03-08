using Newtonsoft.Json;
using QuantConnect.Orders;
using QuantConnect.Orders.Serialization;
using System.Text;

namespace QuantConnect.AlphaStream.Models.Orders
{
    public class AlphaStreamOrderEvent : SerializedOrderEvent
    {
        ///// <summary>
        ///// The unique order event id
        ///// </summary>
        [JsonProperty("id")]
        public override string Id => $"{AlgorithmId}-{HashId}-{OrderEventId}";

        /// <summary>
        /// Id of the order this event comes from.
        /// </summary>
        [JsonProperty("order-id")]
        public string HashId { get; set; }

        public AlphaStreamOrderEvent()
        {
        }

        public AlphaStreamOrderEvent(OrderEvent orderEvent, string algorithmId) : base(orderEvent, algorithmId)
        {
        }

        /// <summary>
        /// Returns a string that represents the current object.
        /// Allows specifying if it should also add complete ID and Symbol. It's useful not to add them when called from parent Order
        /// </summary>
        public string ToString(bool extended)
        {
            var stringBuilder = new StringBuilder();

            if (extended)
            {
                stringBuilder.Append($"Time: {Time} ID: {Id} Symbol: {Symbol} Status: {Status} Quantity {Quantity}");
            }
            else
            {
                stringBuilder.Append($"Time: {Time} OrderId {OrderEventId} Status: {Status} Quantity {Quantity}");
            }

            if (FillQuantity != 0)
            {
                stringBuilder.Append($" FillQuantity: {FillQuantity} FillPrice: {FillPrice} {FillPriceCurrency}");
            }

            if (LimitPrice.HasValue)
            {
                stringBuilder.Append($" LimitPrice: {LimitPrice.Value}");
            }
            if (StopPrice.HasValue)
            {
                stringBuilder.Append($" StopPrice: {StopPrice.Value}");
            }

            if (OrderFeeAmount.HasValue)
            {
                stringBuilder.Append($" OrderFee: {OrderFeeAmount} {OrderFeeCurrency}");
            }

            if (!string.IsNullOrEmpty(Message))
            {
                stringBuilder.Append($" Message: '{Message}'");
            }

            return stringBuilder.ToString();
        }

        /// <summary>
        /// Returns a string that represents the current object.
        /// </summary>
        public override string ToString()
        {
            return ToString(true);
        }
    }
}