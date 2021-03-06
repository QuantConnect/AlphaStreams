![Alpha Streams SDK and Research](http://cdn.quantconnect.com.s3.us-east-1.amazonaws.com/i/github/alpha-streams-sdk.png)
# QuantConnect Alpha Streams API SDK

Welcome to the Alpha Streams API SDK Repository. Here we publish SDK implementations and research for connecting to the Alpha Streams Library and performing batch analysis on crowd-sourced strategies from the QuantConnect community. 

To sign up to the API go to QuantConnect.com/pricing and select the Alpha Stream API add-on from the pricing menu. This data is also available exported daily to a S3 bucket for file-based analysis. 

## Available SDK Languages

Currently there are two SDK implementations; Python and C#. Both are connecting to the same REST API backend. If you are an QuantConnect API client and would like us to publish an SDK in another language please let us know at support@quantconnect.com

### Python SDK Implementation:
The python implementation of the SDK wrapper comes with two research notebooks for performing portfolio analysis([1](https://github.com/QuantConnect/AlphaStream/blob/master/AlphaStream/QuantConnect.AlphaStream.CompositeAlphaAnalysis.ipynb), [2](https://github.com/QuantConnect/AlphaStream/blob/master/AlphaStream/QuantConnect.AlphaStream.AlphaAnalysisNotebook.ipynb)), along with one-["kitchen sink" Jupyter Notebook](https://github.com/QuantConnect/AlphaStream/blob/master/AlphaStream/QuantConnectAlphaStreamsNotebook.ipynb) implementation. 

### C# SDK Implementations:

You can browse the [API implementation](https://github.com/QuantConnect/AlphaStream/tree/master/QuantConnect.AlphaStream), and also a full [demonstration](https://github.com/QuantConnect/AlphaStream/tree/master/QuantConnect.AlphaStream.Demo) of the API and querying it with the C# wrapper.

## Installation Instructions

To install locally, download the zip file with the [latest master](https://github.com/QuantConnect/AlphaStream/archive/master.zip) and unzip it to your favorite location. Alternatively, install [Git](https://git-scm.com/downloads) and clone the repo:

```
git clone https://github.com/QuantConnect/AlphaStream.git
```

This solution depends on [QuantConnect/Lean](https://github.com/QuantConnect/). Consequently, we need to download the zip file with the [latest master](https://github.com/QuantConnect/Lean/archive/master.zip) and unzip it to same location. Alternatively, install [Git](https://git-scm.com/downloads) and clone the repo:

```
git clone https://github.com/QuantConnect/Lean.git
```

## License Agreement

This code is provided only for use with the Alpha Streams Repository and is not available for other commercial use beyond this purpose. It may not be copied, modified or distributed. All intellectual property remains with QuantConnect Corporation. 