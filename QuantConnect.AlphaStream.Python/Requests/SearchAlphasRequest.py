class SearchAlphasRequest(object):
    """ Search for alphas matching this search criteria """

    def __init__(self, *args, **kwargs):
        self.Endpoint = "alpha/search"

        kwargs = kwargs.get('kwargs', kwargs)

        self.Accuracy = kwargs.get('accuracy', None)

        self.AssetClasses = kwargs.get('assetClasses', [])

        self.Author = kwargs.get('author', None)

        self.ExclusiveFeeMinimum = kwargs.get('exclusiveFeeMinimum', None)

        self.ExclusiveFeeMaximum = kwargs.get('exclusiveFeeMaximum', None)

        self.ProjectId = kwargs.get('projectId', None)

        self.SharedFeeMinimum = kwargs.get('sharedFeeMinimum', None)

        self.SharedFeeMaximum = kwargs.get('sharedFeeMaximum', None)

        self.SharpeMinimum = kwargs.get('sharpeMinimum', None)

        self.SharpeMaximum = kwargs.get('sharpeMaximum', None)

        self.Start = kwargs.get('start', 0)

        self.Symbols = kwargs.get('symbols', [])

        self.UniquenessMinimum = kwargs.get('uniquenessMinimum', None)

        self.UniquenessMaximum = kwargs.get('uniquenessMaximum', None)

        self.Tags = kwargs.get('tags', [])

        self.Include = kwargs.get('include', [])

        self.Exclude = kwargs.get('exclude', [])


    def GetPayload(self):
        """ Construct search query data payload from the initialized properties """

        # Common default properties
        payload = {
            "start": self.Start 
        }

        # Optional properties
        if self.Accuracy is not None:
            payload['accuracy'] = self.Accuracy

        if len(self.AssetClasses) > 0:
            payload['asset-classes'] = self.AssetClasses

        if self.Author is not None:
            payload['author'] = self.Author

        if self.ExclusiveFeeMinimum is not None:
            payload['exclusive-fee-minimum'] = self.ExclusiveFeeMinimum

        if self.ExclusiveFeeMaximum is not None:
            payload['exclusive-fee-maximum'] = self.ExclusiveFeeMaximum

        if self.ProjectId is not None:
            payload["project-id"] = self.ProjectId

        if self.SharedFeeMinimum is not None:
            payload['shared-fee-minimum'] = self.SharedFeeMinimum

        if self.SharedFeeMaximum is not None:
            payload['shared-fee-maximum'] = self.SharedFeeMaximum

        if self.SharpeMinimum is not None:
            payload['sharpe-minimum'] = self.SharpeMinimum

        if self.SharpeMaximum is not None:
            payload['sharpe-maximum'] = self.SharpeMaximum

        if len(self.Symbols) > 0:
            payload['symbols'] = self.Symbols

        if self.UniquenessMinimum is not None:
            payload['uniqueness-minimum'] = self.UniquenessMinimum

        if self.UniquenessMaximum is not None:
            payload['uniqueness-maximum'] = self.UniquenessMaximum

        if self.Include is not None:
            payload['include[]'] = self.Include

        if self.Exclude is not None:
            payload['exclude[]'] = self.Exclude

        return payload