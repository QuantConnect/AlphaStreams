class SearchAlphasRequest(object):
    """ Search for alphas matching this search criteria """

    def __init__(self, *args, **kwargs):
        self.Endpoint = "alpha/search"

        kwargs = kwargs.get('kwargs', kwargs)

        self.Start = kwargs.get('start', 0)

        self.Symbols = kwargs.get('symbols', [])

        self.AssetClasses = kwargs.get('assetClasses', [])

        self.Author = kwargs.get('author', None)

        self.IncludedTags = kwargs.get('includedTags', [])

        self.ExcludedTags = kwargs.get('excludedTags', [])

        self.AccuracyMinimum, self.AccuracyMaximum = self._get_range(kwargs, 'accuracy')

        self.ExclusiveFeeMinimum, self.ExclusiveFeeMaximum = self._get_range(kwargs, 'exclusive')

        self.SharedFeeMinimum, self.SharedFeeMaximum = self._get_range(kwargs, 'shared')

        self.ParametersMinimum, self.ParametersMaximum = self._get_range(kwargs, 'parameters')

        self.SharpeMinimum, self.SharpeMaximum = self._get_range(kwargs, 'sharpe')

        self.UniquenessMinimum, self.UniquenessMaximum = self._get_range(kwargs, 'uniqueness')


    def _get_range(self, kwargs, key):

        # If we have the key, it is a list with the minimum and maximum values
        value = kwargs.get(key, [])
        if isinstance(value, list) and len(value) > 0:
            return min(value), max(value)

        return kwargs.get(f'{key}-minimum', None), kwargs.get(f'{key}-maximum', None)


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

        return payload