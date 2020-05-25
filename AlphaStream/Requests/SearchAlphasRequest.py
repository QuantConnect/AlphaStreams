class SearchAlphasRequest(object):
    """ Search for alphas matching this search criteria """

    def __init__(self, *args, **kwargs):
        self.Endpoint = "alpha/search"

        kwargs = kwargs.get('kwargs', kwargs)

        # Start index for batch request
        self.Start = kwargs.get('start', 0)

        # Search for alphas that emit Insights for these symbols
        self.Symbols = kwargs.get('symbols', [])

        # Standard asset classes: Equity, Forex, Crypto, CFD, Options, Futures
        self.AssetClasses = kwargs.get('assetClasses', [])

        # Author ID to find aphas from a specific author
        self.Author = kwargs.get('author', None)

        # Alpha tags to include in the search
        self.IncludedTags = kwargs.get('includedTags', [])

        # Alpha tags to exclude in the search
        self.ExcludedTags = kwargs.get('excludedTags', [])

        # Alpha accuracy in Insight predictions to include in the search
        self.AccuracyMinimum, self.AccuracyMaximum = self._get_range(kwargs, 'accuracy')

        # Range of exclusive licensing fees to include in the search
        self.ExclusiveFeeMinimum, self.ExclusiveFeeMaximum = self._get_range(kwargs, 'exclusive')

        # Range of shared licensing fees to include in the search
        self.SharedFeeMinimum, self.SharedFeeMaximum = self._get_range(kwargs, 'shared')

        # Range of number of parameters in the alpha code to include in the search
        self.ParametersMinimum, self.ParametersMaximum = self._get_range(kwargs, 'parameters')

        # Range of Sharpe ratios to include in the search
        self.SharpeMinimum, self.SharpeMaximum = self._get_range(kwargs, 'sharpe')

        # Range of uniqueness scores to include in the search, based on average alpha returns correlation to all alphas
        self.UniquenessMinimum, self.UniquenessMaximum = self._get_range(kwargs, 'uniqueness')

        # Returns Dynamic Time Warping distance to include in the search
        self.DtwDistanceMinimum, self.DtwDistanceMaximum = self._get_range(kwargs, "dtwDistance")

        # Free trial period range to include in the search
        self.TrialMinimum, self.TrialMaximum = self._get_range(kwargs, "trial")

        # Range of returns correlation values to include in the search
        self.ReturnsCorrelationMinimum, self.ReturnsCorrelationMaximum = self._get_range(kwargs, "returnsCorrelation")


    def _get_range(self, kwargs, key):

        # If we have the key, it is a list with the minimum and maximum values
        value = kwargs.get(key, [])
        if isinstance(value, list) and len(value) > 0:
            return min(value), max(value)

        return kwargs.get(f'{key}Minimum', None), kwargs.get(f'{key}Maximum', None)


    def GetPayload(self):
        """ Construct search query data payload from the initialized properties """

        # Common default properties
        payload = {
            "start": self.Start 
        }

        # Optional properties
        if self.AccuracyMinimum is not None:
            payload['accuracy-minimum'] = self.AccuracyMinimum

        if self.AccuracyMaximum is not None:
            payload['accuracy-maximum'] = self.AccuracyMaximum

        if len(self.AssetClasses) > 0:
            payload['asset-classes'] = self.AssetClasses

        if self.Author is not None:
            payload['author'] = self.Author

        if self.ExclusiveFeeMinimum is not None:
            payload['exclusive-fee-minimum'] = self.ExclusiveFeeMinimum

        if self.ExclusiveFeeMaximum is not None:
            payload['exclusive-fee-maximum'] = self.ExclusiveFeeMaximum

        if self.SharedFeeMinimum is not None:
            payload['shared-fee-minimum'] = self.SharedFeeMinimum

        if self.SharedFeeMaximum is not None:
            payload['shared-fee-maximum'] = self.SharedFeeMaximum

        if self.SharpeMinimum is not None:
            payload['sharpe-minimum'] = self.SharpeMinimum

        if self.SharpeMaximum is not None:
            payload['sharpe-maximum'] = self.SharpeMaximum

        if len(self.Symbols) > 0:
            if (len(self.Symbols) > 1) and (type(self.Symbols) != str):
                symbols = ','.join(self.Symbols)
                payload['symbols'] = symbols
            elif (len(self.Symbols) == 1) and (type(self.Symbols) == list):
                payload['symbols'] = str(self.Symbols)
            else:
                payload['symbols'] = self.Symbols

        if self.UniquenessMinimum is not None:
            payload['uniqueness-minimum'] = self.UniquenessMinimum

        if self.UniquenessMaximum is not None:
            payload['uniqueness-maximum'] = self.UniquenessMaximum

        if self.IncludedTags is not None:
            payload['include'] = self.IncludedTags

        if self.ExcludedTags is not None:
            payload['exclude'] = self.ExcludedTags

        if self.ParametersMinimum is not None:
            payload['parameters-minimum'] = self.ParametersMinimum

        if self.ParametersMaximum is not None:
            payload['parameters-maximum'] = self.ParametersMaximum

        if self.DtwDistanceMinimum is not None:
            payload['out-of-sample-dtw-distance-minimum'] = self.DtwDistanceMinimum

        if self.DtwDistanceMaximum is not None:
            payload['out-of-sample-dtw-distance-maximum'] = self.DtwDistanceMaximum

        if self.TrialMinimum is not None:
            payload['trial-minimum'] = self.TrialMinimum

        if self.TrialMaximum is not None:
            payload['trial-maximum'] = self.TrialMaximum

        if self.ReturnsCorrelationMinimum is not None:
            payload['out-of-sample-returns-correlation-minimum'] = self.ReturnsCorrelationMinimum

        if self.ReturnsCorrelationMaximum is not None:
            payload['out-of-sample-returns-correlation-maximum'] = self.ReturnsCorrelationMaximum


        return payload