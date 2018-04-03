import numpy as np 
import pandas as pd


# def from_pivot(df_pivot):
#     df = df_pivot.stack().reset_index()
#     print(df.columns)
#     del df_pivot
    
#     df = df[['DATE', 'ATM_ID', 0]]
#     df.columns = ['DATE', 'ATM_ID', 'CLIENT_OUT']
    
#     return df

# from_pivot(df_pivot)


def CreateColumnsOfMeans(df, offsets=[7, 14, 21, 28, 35], window=61):
    def HelperForMeans(df_pivot, offset):
        a = np.empty((df_pivot.shape[0], offset))
        a[:] = np.nan

        data = np.hstack([a, df_pivot.values[:, :-offset]])

        return data.reshape(-1)

    
    def to_pivot(df):
         return pd.pivot_table(df, values='CLIENT_OUT', index='ATM_ID', columns='DATE')

    
    df_pivot = to_pivot(df)
    df_pivot = df_pivot.T.rolling(window=61).mean().T 
    
#     return HelperForMeans(df_pivot, 7)
    return pd.DataFrame(np.array([HelperForMeans(df_pivot, offset) for offset in offsets]).T,
                        columns=['mean_minus_7', 'mean_minus_14', 'mean_minus_21', 'mean_minus_28', 'mean_minus_35'])

    

# df_for_means = CreateColumnsOfMeans(df)