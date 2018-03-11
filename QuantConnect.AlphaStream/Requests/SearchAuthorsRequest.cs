using System;
using System.Collections.Generic;
using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Search Author database by query filters to locate researchers according to criteria.
    /// </summary>
    [Endpoint(Method.GET, "alpha/author/search")]
    public class SearchAuthorsRequest : AttributeRequest<List<Author>>
    {
        /// <summary>
        /// Best guess geographic location of the Author based on the IP address.
        /// </summary>
        [QueryParameter("location")]
        public string Location { get; set; }

        /// <summary>
        /// Preferred programming language for the primary Author.
        /// </summary>
        [QueryParameter("languages")]
        public List<string> Languages { get; set; } = new List<string>();

        /// <summary>
        /// Search the Author biography information for this text.
        /// </summary>
        [QueryParameter("biography")]
        public string Biography { get; set; }

        /// <summary>
        /// Number of Alphas the Author has listed.
        /// </summary>
        [QueryParameter("alphas")]
        public NumberRange<int> Alphas { get; set; }

        /// <summary>
        /// Unix timestamp of the Author registration on QuantConnect.
        /// </summary>
        [QueryParameter("signed-up")]
        public DateRange<DateTime> SignedUp { get; set; }

        /// <summary>
        /// Unix timestamp of the Author last login on QuantConnect.
        /// </summary>
        [QueryParameter("last-login")]
        public DateRange<DateTime> LastLogin { get; set; }

        /// <summary>
        /// Number of discussions started on QuantConnect.
        /// </summary>
        [QueryParameter("forum-discussions")]
        public NumberRange<int> ForumDiscussions { get; set; }

        /// <summary>
        /// Number of comments created on QuantConnect.
        /// </summary>
        [QueryParameter("forum-comments")]
        public NumberRange<int> ForumComments { get; set; }

        /// <summary>
        /// Range of the number of projects.
        /// </summary>
        [QueryParameter("projects")]
        public NumberRange<int> Projects { get; set; }
    }
}