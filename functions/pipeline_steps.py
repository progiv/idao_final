from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
class FinalStepForSubmission(BaseEstimator, TransformerMixin):
    """
    FINAL
    """
    
    def fit(self, X, y=None):
        return self

    def predict(self, X):
        X = X[['DATE', "ATM_ID", "y_predict"]]
        X.columns = ['DATE', "ATM_ID", "CLIENT_OUT"]
        print(len(np.unique(X.ATM_ID)))
        print("FinalStepForSubmission Finished")
        return X
        
class WrapperForEstimator(BaseEstimator, TransformerMixin):
    """
    FINAL
    """
    def __init__(self, estimator):
        self.estimator = estimator
    
    
    def fit(self, X, y=None):
        #indices_without_nan = X.isnull().any(axis=1)
        #indices_without_nan = X.index[indices_without_nan]
        
        #X.drop(axis=0, index=indices_without_nan, inplace=True)
        #y.drop(axis=0, index=indices_without_nan, inplace=True)
        
        #print("WrapperForEstimator fit called")
        #print(X.columns)
        #print(sum(X.drop(['DATE',  'ATM_ID', 'CLIENT_OUT'],).isna().any(axis=1)), sum(y.isna().any(axis=1)))
        XX = X.drop(['DATE',  'ATM_ID', 'CLIENT_OUT'], axis=1, inplace=False)
        self.estimator.fit(XX, y)
        
        return self

    def transform(self, X):
        print("WrapperForEstimator transform called")
        
        y_pred = self.estimator.predict(X.drop(['DATE',  'ATM_ID', 'CLIENT_OUT'], axis=1, inplace=False))
        
        X_tr = X.copy()
        X_tr['y_predict'] = y_pred
        print("Transform from estimator Finished")
        return X_tr