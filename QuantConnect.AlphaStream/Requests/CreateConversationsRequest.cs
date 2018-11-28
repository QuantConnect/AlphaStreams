using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Create a conversation thread.
    /// Start a conversation with the author(s) of the alpha via email. Quickly solve reconciliation issues or design automated filter questions.
    /// </summary>
    [Endpoint(Method.GET, "/alpha/{id}/conversations/create")]
    public class CreateConversationsRequest : AttributeRequest<ApiResponse>
    {
        /// <summary>
        /// Unique id hash of an Alpha published to the marketplace.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }

        /// <summary>
        /// Email that is going to be used to send the replies from the author(s).
        /// </summary>
        [QueryParameter("from")]
        public string From { get; set; }

        /// <summary>
        /// The subject of the thread, this is going to be used for the email.
        /// </summary>
        [QueryParameter("subject")]
        public string Subject { get; set; }

        /// <summary>
        /// Message to be sent to the author(s)
        /// </summary>
        [QueryParameter("message")]
        public string Message { get; set; }

        /// <summary>
        /// Comma separated list of emails that are going to be copied into the author(s) replies.
        /// </summary>
        [QueryParameter("cc")]
        public string CC { get; set; } = string.Empty;
    }
}