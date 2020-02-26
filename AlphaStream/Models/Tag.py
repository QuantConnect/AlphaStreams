class Tag:
    def __init__(self, result):
        self.TagName = result.get('tag', '')
        self.Matches = result.get('matches', '')

    def __repr__(self):
        return f'"{self.TagName}" returned {self.Matches} matches'