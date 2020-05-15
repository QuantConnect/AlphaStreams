class Tag:
    """ Alpha tag and the number of alphas with the tag """
    def __init__(self, result):
        self.TagName = result.get('tag', '')
        self.Matches = result.get('matches', 0)

    def __repr__(self):
        return f'"{self.TagName}" returned {self.Matches} matches'