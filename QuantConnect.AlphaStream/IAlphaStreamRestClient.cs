using System.Threading.Tasks;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream
{
    public interface IAlphaStreamRestClient
    {
        Task<T> Execute<T>(IRequest<T> request);
    }
}