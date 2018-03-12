using System.Collections.Generic;
using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Search endpoint for locating Alphas matching search criteria. All input values are optional and are joined with a logical AND for the filtered results.
    /// </summary>
    [Endpoint(Method.GET, "alpha/search")]
    public class SearchAlphasRequest : AttributeRequest<List<Alpha>>
    {
        /// <summary>
        /// Search for Alphas which have a specific accuracy range.
        /// </summary>
        [QueryParameter("accuracy")]
        public NumberRange<double> Accuracy { get; set; }

        /// <summary>
        /// Array of asset classes to search.
        /// </summary>
        [QueryParameter("assets-classes")]
        public List<AssetClass> Assets { get; set; } = new List<AssetClass>();

        /// <summary>
        /// Fee filter on the listed Alphas in a specific range.
        /// </summary>
        [QueryParameter("fee")]
        public NumberRange<decimal> Fee { get; set; }

        /// <summary>
        /// Search for Alphas created by a specific Project.
        /// </summary>
        [QueryParameter("project-id")]
        public long? ProjectId { get; set; }

        /// <summary>
        /// Hash Author identifier to locate.
        /// </summary>
        [QueryParameter("author")]
        public string Author { get; set; }

        /// <summary>
        /// Search for Alphas which utilize specific symbols. QuantConnect symbol identifier code.
        /// </summary>
        [QueryParameter("symbols")]
        public List<string> Symbols { get; set; } = new List<string>();

        /// <summary>
        /// Search for Alphas which have a specific sharpe ratio range.
        /// </summary>
        [QueryParameter("sharpe")]
        public NumberRange<double> Sharpe { get; set; }

        /// <summary>
        /// Search for Alphas which fall into a specific uniqueness range relative to existing portfolio.
        /// </summary>
        [QueryParameter("uniqueness")]
        public NumberRange<double> Uniqueness { get; set; }

        /// <summary>
        /// The start index of the search. This is used to support pagination
        /// </summary>
        [QueryParameter("start")]
        public int Start { get; set; }
    }
}