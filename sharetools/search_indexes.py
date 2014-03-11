from haystack import indexes
from sharetools.models import Asset

class AssetIndex(indexes.BasicSearchIndex, indexes.Indexable):
    def get_model(self):
        return Asset