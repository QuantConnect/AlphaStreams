using System.Diagnostics;
using NUnit.Framework;

namespace QuantConnect.AlphaStream.Tests
{
    [SetUpFixture]
    public class Setup
    {
        [OneTimeSetUp]
        public void Tracing()
        {
            // turn request/response tracing
            AlphaStreamRestClient.RequestTracingEnabled = true;
            AlphaStreamRestClient.ResponseTracingEnabled = true;

            // route trace messages to console
            Trace.Listeners.Add(new ConsoleTraceListener());
        }
    }
}