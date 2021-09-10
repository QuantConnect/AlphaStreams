using QuantConnect.AlphaStream.Infrastructure;
using RestSharp;
using System.Collections.Generic;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Fetch Alpha equity curve consisting of both backtest and live performance
    /// </summary>

    [Endpoint(Method.GET, "/alpha/{id}/equity")]

    public class GetAlphaEquityCurveRequest : AttributeRequest<List<object[]>>
    {
        /// <summary>
        /// Unique id hash of an Alpha published to the marketplace.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }

        /// <summary>
        /// Preferred date format
        /// </summary>
        [QueryParameter("date-format")]
        public string DateFormat { get; set; } = "date";

        /// <summary>
        /// Preferred format of returned equity curve
        /// </summary>
        [QueryParameter("format")]
        public string Format { get; set; } = "json";

        /// <summary>
        /// Preferred content of returned equity curve.
        /// If False, returns data of one single Alpha with the following sampling: in sample, out of sample, and live trading
        /// If True, returns unified data of all versions of this Alpha with the live trading sampling only
        /// </summary>
        [QueryParameter("unified")]
        public bool Unified { get; set; } = true;

        /// <summary>
        /// Returns a string that represents the GetAlphaEquityCurveRequest object
        /// </summary>
        /// <returns>A string that represents the GetAlphaEquityCurveRequest object</returns>
        public override string ToString()
        {
            return $"{Id}: Date/time format {DateFormat} Data format: {Format}";
        }
    }
}