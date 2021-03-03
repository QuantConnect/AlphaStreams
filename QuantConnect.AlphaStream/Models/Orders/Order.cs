using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using QuantConnect.Util;

namespace QuantConnect.AlphaStream.Models.Orders
{
    public class Order
    {
        /// <summary>
        /// The unique order id
        /// </summary>
        [JsonProperty("id")]
        public string Id => $"{AlgorithmId}-{OrderId}";

        /// <summary>
        /// Algorithm Id, BacktestId or DeployId
        /// </summary>
        [JsonProperty("algorithm-id")]
        public string AlgorithmId { get; set; }

        /// <summary>
        /// Order ID
        /// </summary>
        [JsonProperty("order-id")]
        public int OrderId { get; set; }

        /// <summary>
        /// Order id to process before processing this order.
        /// </summary>
        [JsonProperty("contingent-id")]
        public int ContingentId { get; set; }

        /// <summary>
        /// Brokerage Id for this order for when the brokerage splits orders into multiple pieces
        /// </summary>
        [JsonProperty("broker-id")]
        public List<string> BrokerId { get; set; } = new List<string>();

        /// <summary>
        /// Symbol of the Asset
        /// </summary>
        [JsonProperty("symbol")]
        public string Symbol { get; set; }

        /// <summary>
        /// Price of the Order.
        /// </summary>
        [JsonProperty("price")]
        public decimal Price { get; set; }

        /// <summary>
        /// Currency for the order price
        /// </summary>
        [JsonProperty("price-currency")]
        public string PriceCurrency { get; set; }

        /// <summary>
        /// Gets the utc time this order was created. Alias for <see cref="Time"/>
        /// </summary>
        [JsonProperty("created-time"), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime CreatedTime { get; set; }

        /// <summary>
        /// Gets the utc time the last fill was received, or null if no fills have been received
        /// </summary>
        [JsonProperty("last-fill-time", NullValueHandling = NullValueHandling.Ignore), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime? LastFillTime { get; set; }

        /// <summary>
        /// Gets the utc time this order was last updated, or null if the order has not been updated.
        /// </summary>
        [JsonProperty("last-update-time", NullValueHandling = NullValueHandling.Ignore), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime? LastUpdateTime { get; set; }

        /// <summary>
        /// Gets the utc time this order was canceled, or null if the order was not canceled.
        /// </summary>
        [JsonProperty("canceled-time", NullValueHandling = NullValueHandling.Ignore), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime? CanceledTime { get; set; }

        /// <summary>
        /// Number of shares to execute.
        /// </summary>
        [JsonProperty("quantity")]
        public decimal Quantity { get; set; }

        /// <summary>
        /// Order Type
        /// </summary>
        [JsonProperty("type"), JsonConverter(typeof(StringEnumConverter), true)]
        public OrderType Type { get; set; }

        /// <summary>
        /// Status of the Order
        /// </summary>
        [JsonProperty("status"), JsonConverter(typeof(StringEnumConverter), true)]
        public OrderStatus Status { get; set; }

        /// <summary>
        /// Tag the order with some custom data
        /// </summary>
        [DefaultValue(""), JsonProperty("tag", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public string Tag { get; set; }

        /// <summary>
        /// Order Direction Property based off Quantity.
        /// </summary>
        [JsonProperty("direction"), JsonConverter(typeof(StringEnumConverter), true)]
        public OrderDirection Direction { get; set; }

        /// <summary>
        /// The current price at order submission time
        /// </summary>
        [JsonProperty("submission-last-price", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public decimal SubmissionLastPrice { get; set; }

        /// <summary>
        /// The ask price at order submission time
        /// </summary>
        [JsonProperty("submission-ask-price", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public decimal SubmissionAskPrice { get; set; }

        /// <summary>
        /// The bid price at order submission time
        /// </summary>
        [JsonProperty("submission-bid-price", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public decimal SubmissionBidPrice { get; set; }

        /// <summary>
        /// The current stop price
        /// </summary>
        [JsonProperty("stop-price", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public decimal? StopPrice { get; set; }

        /// <summary>
        /// Signal showing the "StopLimitOrder" has been converted into a Limit Order
        /// </summary>
        [JsonProperty("stop-triggered", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public bool? StopTriggered { get; set; }

        /// <summary>
        /// The current limit price
        /// </summary>
        [JsonProperty("limit-price", DefaultValueHandling = DefaultValueHandling.Ignore)]
        public decimal? LimitPrice { get; set; }

        /// <summary>
        /// The time in force type
        /// </summary>
        [JsonProperty("time-in-force-type")]
        public string TimeInForceType { get; set; }

        /// <summary>
        /// The time in force expiration time if any
        /// </summary>
        [JsonProperty("time-in-force-expiry", DefaultValueHandling = DefaultValueHandling.Ignore), JsonConverter(typeof(DoubleUnixSecondsDateTimeJsonConverter))]
        public DateTime? TimeInForceExpiry { get; set; }

        /// <summary>
        /// Specifies the source of this order, live trading/backtesting/out of sample
        /// </summary>
        [JsonProperty("source")]
        public string Source { get; set; }

        /// <summary>
        /// The orders <see cref="OrderEvent"/>
        /// </summary>
        [JsonProperty("events")]
        public List<OrderEvent> OrderEvents { get; set; } = new List<OrderEvent>();

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
                stringBuilder.Append(string.Join("},{", OrderEvents.Select(orderEvent => orderEvent.ToString(extended:false))));
                stringBuilder.Append("}]");
            }

            return stringBuilder.ToString();
        }
    }
}
