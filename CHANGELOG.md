## ![AlphaStream](https://cdn.quantconnect.com/web/i/alpha/alpha_header_rev0.png) Alpha Streams API Change Log

### Introduction ##

The Alpha Streams API SDK is a helper package for connecting to the QuantConnect Alpha Streams marketplace and consuming insights from

----

### API v0.5 - [Specification](QuantConnect.API.Specification/QuantConnect_Alpha_0.5_swagger.yaml)

#### Features:
 - Added Historical alpha prices endpoint: `/alpha/{id}/prices`.
 - Added Live runtime errors track record: `/alpha/{id}/errors`.
 - Added `Insight.CloseTime` as short cut for start of insight + in-market period (excluding holidays, after hours).  
 - Added `Alpha.Status` property. After 10 runtime errors Alphas automatically will be stopped and their status updated from `running` to `stopped`.
 - Added `Alpha.AuthorTrading` property to indicate if the Author is actively trading the same signal.
 - Added `Insight.Group` property: when insights are intended to be traded together they share a common group hash (e.g. pairs trading).
 - Added `Insight.SourceModel` property to support alpha models with multiple signals to be joined together. Source Model is the class name.
 
#### Bug Fixes:
 - Fixed inconsistencies with naming time indexed properties. `CreatedTime`, `LastModifiedTime`.
 - Renamed `Alpha.ListedDate` -> `Alpha.ListedTime`
 - Renamed `Insight.Reference` to more specific `ReferenceValue` to path way for future insight types.