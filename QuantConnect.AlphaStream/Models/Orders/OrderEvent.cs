using System;
using System.ComponentModel;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream.Models.Orders
{
    public class OrderEvent
    {
        /// <summary>
        /// The unique order event id
        /// </summary>
        [JsonProperty("id")]
        public string Id => $"{AlgorithmId}-{OrderId}-{OrderEventId}";

        /// <summary>
        /// Algorithm Id, BacktestId or DeployId
        /// </summary>
        [JsonProperty("algorithm-id")]
        public string AlgorithmId { get; set; }

        /// <summary>
        /// Id of the order this event comes from.
        /// </summary>
        [JsonProperty("order-id")]
        public int OrderId { get; set; }

        /// <summary>
        /// The unique order event id for each order
        /// </summary>
        [JsonProperty("order-event-id")]
        public int OrderEventId { get; set; }

        /// <summary>
        /// Easy access to the order symbol associated with this event.
        /// </summary>
        [JsonProperty("symbol")]
        public string Symbol { get; set; }

        /// <summary>
        /// The time of this event in unix timestamp
        /// </summary>
        [JsonProperty("time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime Time { get; set; }

        /// <summary>
        /// Status message of the order.
        /// </summary>
        [JsonProperty("status"), JsonConverter(typeof(StringEnumConverter), true)]
        public OrderStatus Status { get; set; }

        /// <summary>
        /// The fee amount associated with the order
        /// </summary>
        [JsonProperty("order-fee-amount")]
        public decimal OrderFeeAmount { get; set; }

        /// <summary>
        /// The fee currency associated with the order
        /// </summary>
        [JsonProperty("order-fee-currency")]
        public string OrderFeeCurrency { get; set; }

        /// <summary>
        /// Fill price information about the order
        /// </summary>
        [JsonProperty("fill-price")]
        public decimal FillPrice { get; set; }

        /// <summary>
        /// Currency for the fill price
        /// </summary>
        [JsonProperty("fill-price-currency")]
        public string FillPriceCurrency { get; set; }

        /// <summary>
        /// Number of shares of the order that was filled in this event.
        /// </summary>
        [JsonProperty("fill-quantity")]
        public decimal FillQuantity { get; set; }

        /// <summary>
        /// Order direction.
        /// </summary>
        [JsonProperty("direction"), JsonConverter(typeof(StringEnumConverter), true)]
        public OrderDirection Direction { get; set; }

        /// <summary>
        /// Any message from the exchange.
        /// </summary>
        [DefaultValue(""), JsonProperty("message", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public string Message { get; set; }

        /// <summary>
        /// True if the order event is an assignment
        /// </summary>
        [JsonProperty("is-assignment")]
        public bool IsAssignment { get; set; }

        /// <summary>
        /// The current order quantity
        /// </summary>
        [JsonProperty("quantity")]
        public decimal Quantity { get; set; }

        /// <summary>
        /// The current stop price
        /// </summary>
        [JsonProperty("stop-price", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public decimal? StopPrice { get; set; }

        /// <summary>
        /// The current limit price
        /// </summary>
        [JsonProperty("limit-price", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public decimal? LimitPrice { get; set; }

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

            if (OrderFeeAmount != 0m) stringBuilder.Append($" OrderFee: {OrderFeeAmount} {OrderFeeCurrency}");

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
