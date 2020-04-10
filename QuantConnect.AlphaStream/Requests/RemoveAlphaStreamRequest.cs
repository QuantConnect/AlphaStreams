namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Request used to remove an alpha being streamed
    /// </summary>
    public class RemoveAlphaStreamRequest
    {
        /// <summary>
        /// The alpha id stream to remove
        /// </summary>
        public string AlphaId { get; set; }
    }
}
