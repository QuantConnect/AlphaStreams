namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Request used to add a new alpha to stream
    /// </summary>
    public class AddAlphaStreamRequest
    {
        /// <summary>
        /// The alpha id stream to request
        /// </summary>
        public string AlphaId { get; set; }
    }
}
