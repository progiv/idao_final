import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


"""
FOR TRAIN USE:
df = CreatingNewPivotTable_TRAIN_ONLY(df, window_size=15)

FOR TEST USE:
df, is_small = CreatingNewPivotTable_TEST(df, window_size=15)
"""

def PlotWithChanges(df, df_zeroes_window, index=0, plot=True):
    df_pivot = pd.pivot_table(df, values='CLIENT_OUT', index='ATM_ID', columns='DATE')
    df_zeroes = FindZeroes(df_pivot, window_size=df_zeroes_window)
    
    zeroes = df_zeroes.loc[index, :].values
        
    if plot:
        plt.figure(figsize=(15, 15))
        plt.plot(df_pivot.loc[index, :].values / df_pivot.loc[index, :].values.mean())

        plt.plot(zeroes)
        plt.show()
    
    return ReturnRangesForChanges(zeroes, df_zeroes_window)


def FindZeroes(df_pivot, window_size):
    return df_pivot.T.rolling(window=window_size).mean().T == 0

def ReturnRangesForChanges(zeroes_list, zeroes_window):
    ranges = []

    start_iter = 0
    live = True

    for i, x in enumerate(zeroes_list):
        if live:
            if x == 1:
                ranges.append([start_iter, i - zeroes_window + 1])
                live = False
        else:
            if x == 0:
                start_iter = i
                live = True

    ranges.append([start_iter, i])
    
    return ranges



def ChangeFirstZeroesToNone(row):
    index = row.nonzero()[0][0]
    row[:index] = None
    return row


def CleanDataFrame_TRAIN_ONLY(df, window_size=15):    
    """
    HOW TO USE:
    
    
    df = CleanDataFrame_TRAIN_ONLY(df, window_size=15)
    """

    
    ids = np.unique(df.ATM_ID)
    df_pivot = pd.pivot_table(df, values='CLIENT_OUT', index='ATM_ID', columns='DATE')
    
    # remove first zeroes
    df_pivot = df_pivot.apply(ChangeFirstZeroesToNone, axis=1)
    
    
    df_zeroes = FindZeroes(df_pivot, window_size=window_size)
    
    final_pivot = pd.DataFrame(columns=df_pivot.columns)
    
    counter = 0
    for i in ids:
        zeroes = df_zeroes.loc[i, :].values
        ranges = ReturnRangesForChanges(zeroes, window_size)
                
        for index, range_ in enumerate(ranges):
            if range_[1] - range_[0] < 62:
                continue
            
            data = df_pivot.loc[i, :].copy()
            data[:range_[0]] = None
            data[range_[1]:] = None
#             print(range_, counter)
            final_pivot.loc[counter, :] = data
    
            counter += 1
            

    del df_zeroes
    
    
    # from pivot back to long df
    final_df = final_pivot.stack().reset_index()
    del final_pivot
    
    final_df = final_df[['DATE', 'level_0', 0]]
    final_df.columns = df.columns
    
    return final_df



def CleanDataFrame_TEST(df, window_size=15):
    """
    HOW TO USE:
    
    
    
    df, is_small = CleanDataFrame_TEST(df, window_size=15)
    """

    ids = np.unique(df.ATM_ID)
    df_pivot = pd.pivot_table(df, values='CLIENT_OUT', index='ATM_ID', columns='DATE')
    
    df_pivot = df_pivot.apply(ChangeFirstZeroesToNone, axis=1)
    df_zeroes = FindZeroes(df_pivot, window_size=window_size)
    final_pivot = pd.DataFrame(columns=df_pivot.columns)

    renumerate_dict = {}
    
    columns_size = df_pivot.shape[1]
        
    counter = 0
    for i in ids:
        zeroes = df_zeroes.loc[i, :].values
        ranges = ReturnRangesForChanges(zeroes, window_size)[-1]
            
        renumerate_dict[counter] = i
        
        print(ranges)
        
        data = df_pivot.loc[i, :].copy()
        
        if ranges[1] - ranges[0] < 62:
            
            print(i)
            print(ranges)
            
            if ranges[1] - ranges[0] < 7:
                data[:] = np.mean(df_pivot.loc[i, np.range(ranges[-1][0], ranges[-1][1])].values)
            else:
                for index in range(8, 100):
                    data[-index] = data[-index + 7]        
        
        data[:(ranges[1] - 61)] = None
        data[ranges[1]:] = None
        
        final_pivot.loc[counter, :] = data

        counter += 1


    del df_zeroes
    
    
    # from pivot back to long df
    final_df = final_pivot.stack().reset_index()
    del final_pivot
    
    final_df = final_df[['DATE', 'level_0', 0]]
    final_df.columns = df.columns
    
    final_df.ATM_ID = final_df.ATM_ID.map(renumerate_dict)
    
    return final_df
