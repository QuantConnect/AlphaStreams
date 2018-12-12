using System;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Event arguments fired when a new heartbeat is received by the streaming client
    /// </summary>
    public class HeartbeatReceivedEventArgs : EventArgs
    {
        /// <summary>
        /// Gets the alpha id that produced the heartbeat
        /// </summary>
        public string AlphaId { get; }

        /// <summary>
        /// Gets the algorithm id for the given alpha
        /// </summary>
        public string AlgorithmId { get; }

        /// <summary>
        /// Gets the machine time of the heartbeat
        /// </summary>
        public DateTime MachineTime { get; set; }

        /// <summary>
        /// Initializes a new instance of the <see cref="HeartbeatReceivedEventArgs"/> class
        /// </summary>
        /// <param name="alphaId">The alpha id that produced the heartbeat</param>
        /// <param name="algorithmId">The algorithm id for the given alpha</param>
        /// <param name="machineTime">The machine time of the heartbeat</param>
        public HeartbeatReceivedEventArgs(string alphaId, string algorithmId, DateTime? machineTime)
        {
            AlphaId = alphaId;
            AlgorithmId = algorithmId;
            if (machineTime.HasValue)
            {
                MachineTime = machineTime.Value;
            }
        }
    }
}