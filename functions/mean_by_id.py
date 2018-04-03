"""
Returns one feature column
"""
from sklearn.base import BaseEstimator, TransformerMixin
class MeanByIdFeature(BaseEstimator, TransformerMixin):
    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        return X['CLIENT_OUT'].groupby(X['ATM_ID']).transform('mean')