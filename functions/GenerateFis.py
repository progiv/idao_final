import pandas as pd
import numpy as np

def GenerateFis(df_init):
    df = df_init.copy()
    
    def holiday(df):
        condition_holiday = (
        (df.DATE.dt.month == 1) & ((df.DATE.dt.day >= 1) & (df.DATE.dt.day <= 8)) # winter
        | (df.DATE.dt.month == 2) & ((df.DATE.dt.day >= 21) & (df.DATE.dt.day <= 25)) # around 23 feb
        | (df.DATE.dt.month == 3) & ((df.DATE.dt.day >= 6) & (df.DATE.dt.day <= 10)) # around 8 mar
        | (df.DATE.dt.month == 5) & ((df.DATE.dt.day >= 1) & (df.DATE.dt.day <= 10)) # may
        | (df.DATE.dt.month == 6) & ((df.DATE.dt.day >= 10) & (df.DATE.dt.day <= 14)) # around 12 june
        | (df.DATE.dt.month == 11) & ((df.DATE.dt.day >= 2) & (df.DATE.dt.day <= 6)) # around 4 nov
        )
        return condition_holiday + 0
    
    def shift(df2, i):
        df = df2.copy()
        
        for n in [1,2,3,4,5]:
            N = n + i - 1
#             print("i", i)
#             print("N", N)
            df['same_day_{}_week_ago'.format(N)] = df.groupby(['ATM_ID'])['CLIENT_OUT'].shift(7*N).astype(np.float)
            df['mean_{}_week_ago'.format(N)] = df.groupby(['ATM_ID'])['mean'].shift(7*N).astype(np.float)
            df['std_{}_week_ago'.format(N)] = df.groupby(['ATM_ID'])['std'].shift(7*N).astype(np.float)
            
            if n != 1:
                df['same_day_{}_week_ago_plusday'.format(N)] = df.groupby(['ATM_ID'])['CLIENT_OUT'].shift(7*N-1).astype(np.float)
                
            df['same_day_{}_week_ago_minusday'.format(N)] = df.groupby(['ATM_ID'])['CLIENT_OUT'].shift(7*N+1).astype(np.float)
        
        
        
        return df
    
    df['month_of_year'] = df.DATE.dt.month
    df['day_of_week'] = df.DATE.dt.dayofweek
#    df['day_of_month'] = df.DATE.dt.day
    df['week_of_month'] = ((df.DATE.dt.day  - 1) // 7 + 1)
    
    df['weekend_dummy'] = (df.DATE.dt.dayofweek.isin([5,6]) + 0)
    df['holiday_dummy'] = holiday(df)
    
    list_dummies = ['day_of_week', 
#                 'day_of_month',
                'week_of_month',
                'month_of_year']
    
    df = pd.get_dummies(df, columns=list_dummies)
    
    df['mean'] = df.CLIENT_OUT.rolling(window=7, center=False).mean()
    df['std'] = df.CLIENT_OUT.rolling(window=7, center=False).std()
    
    dfs = []
    
    for i in range(1, 6):
#         print(i)
        dfs.append(shift(df, i))
    
    for i in range(len(dfs)):
        dfs[i] = dfs[i].drop('mean', 1)
        dfs[i] = dfs[i].drop('std', 1)
#         dfs[i] = dfs[i].dropna(subset=dfs[i].columns.drop('CLIENT_OUT'))
    
    return dfs





def GenerateFisSasha(df_init):
    df = df_init.copy()
    
    def holiday(df):
        condition_holiday = (
        (df.DATE.dt.month == 1) & ((df.DATE.dt.day >= 1) & (df.DATE.dt.day <= 8)) # winter
        | (df.DATE.dt.month == 2) & ((df.DATE.dt.day >= 21) & (df.DATE.dt.day <= 25)) # around 23 feb
        | (df.DATE.dt.month == 3) & ((df.DATE.dt.day >= 6) & (df.DATE.dt.day <= 10)) # around 8 mar
        | (df.DATE.dt.month == 5) & ((df.DATE.dt.day >= 1) & (df.DATE.dt.day <= 10)) # may
        | (df.DATE.dt.month == 6) & ((df.DATE.dt.day >= 10) & (df.DATE.dt.day <= 14)) # around 12 june
        | (df.DATE.dt.month == 11) & ((df.DATE.dt.day >= 2) & (df.DATE.dt.day <= 6)) # around 4 nov
        )
        return condition_holiday + 0
    
    def shift(df2, i):
        df = df2.copy()
        
        for n in [1,2,3,4,5]:
            N = n + i - 1
#             print("i", i)
#             print("N", N)
            df['same_day_{}_week_ago'.format(N)] = df.groupby(['ATM_ID'])['CLIENT_OUT'].shift(7*N).astype(np.float)
            df['mean_{}_week_ago'.format(N)] = df.groupby(['ATM_ID'])['mean'].shift(7*N).astype(np.float)
            df['std_{}_week_ago'.format(N)] = df.groupby(['ATM_ID'])['std'].shift(7*N).astype(np.float)
            
            if n != 1:
                df['same_day_{}_week_ago_plusday'.format(N)] = df.groupby(['ATM_ID'])['CLIENT_OUT'].shift(7*N-1).astype(np.float)
                
            df['same_day_{}_week_ago_minusday'.format(N)] = df.groupby(['ATM_ID'])['CLIENT_OUT'].shift(7*N+1).astype(np.float)
        
        df[['weekend_dummy', 'holiday_dummy',
       'day_of_week_0', 'day_of_week_1', 'day_of_week_2', 'day_of_week_3',
       'day_of_week_4', 'day_of_week_5', 'day_of_week_6', 'week_of_month_1',
       'week_of_month_2', 'week_of_month_3', 'week_of_month_4',
       'week_of_month_5', 'month_of_year_1', 'month_of_year_2',
       'month_of_year_3', 'month_of_year_4', 'month_of_year_5',
       'month_of_year_6', 'month_of_year_7', 'month_of_year_8',
       'month_of_year_9', 'month_of_year_10', 'month_of_year_11',
       'month_of_year_12']] = df[['weekend_dummy', 'holiday_dummy',
       'day_of_week_0', 'day_of_week_1', 'day_of_week_2', 'day_of_week_3',
       'day_of_week_4', 'day_of_week_5', 'day_of_week_6', 'week_of_month_1',
       'week_of_month_2', 'week_of_month_3', 'week_of_month_4',
       'week_of_month_5', 'month_of_year_1', 'month_of_year_2',
       'month_of_year_3', 'month_of_year_4', 'month_of_year_5',
       'month_of_year_6', 'month_of_year_7', 'month_of_year_8',
       'month_of_year_9', 'month_of_year_10', 'month_of_year_11',
       'month_of_year_12']].astype(np.float32)
        
        df[['weekend_dummy', 'holiday_dummy',
       'day_of_week_0', 'day_of_week_1', 'day_of_week_2', 'day_of_week_3',
       'day_of_week_4', 'day_of_week_5', 'day_of_week_6', 'week_of_month_1',
       'week_of_month_2', 'week_of_month_3', 'week_of_month_4',
       'week_of_month_5', 'month_of_year_1', 'month_of_year_2',
       'month_of_year_3', 'month_of_year_4', 'month_of_year_5',
       'month_of_year_6', 'month_of_year_7', 'month_of_year_8',
       'month_of_year_9', 'month_of_year_10', 'month_of_year_11',
       'month_of_year_12']] = df[['weekend_dummy', 'holiday_dummy',
       'day_of_week_0', 'day_of_week_1', 'day_of_week_2', 'day_of_week_3',
       'day_of_week_4', 'day_of_week_5', 'day_of_week_6', 'week_of_month_1',
       'week_of_month_2', 'week_of_month_3', 'week_of_month_4',
       'week_of_month_5', 'month_of_year_1', 'month_of_year_2',
       'month_of_year_3', 'month_of_year_4', 'month_of_year_5',
       'month_of_year_6', 'month_of_year_7', 'month_of_year_8',
       'month_of_year_9', 'month_of_year_10', 'month_of_year_11',
       'month_of_year_12']].multiply(df['mean_5_week_ago'], axis=0)

        return df
    
    df['month_of_year'] = df.DATE.dt.month
    df['day_of_week'] = df.DATE.dt.dayofweek
#    df['day_of_month'] = df.DATE.dt.day
    df['week_of_month'] = ((df.DATE.dt.day  - 1) // 7 + 1)
    
    df['weekend_dummy'] = (df.DATE.dt.dayofweek.isin([5,6]) + 0)
    df['holiday_dummy'] = holiday(df)
    
    list_dummies = ['day_of_week', 
#                 'day_of_month',
                'week_of_month',
                'month_of_year']
    
    df = pd.get_dummies(df, columns=list_dummies)
#     df = df.va * df.CLIENT_OUT.rolling(window=7, center=False).mean()
    lis = ['weekend_dummy', 'holiday_dummy',
       'day_of_week_0', 'day_of_week_1', 'day_of_week_2', 'day_of_week_3',
       'day_of_week_4', 'day_of_week_5', 'day_of_week_6', 'week_of_month_1',
       'week_of_month_2', 'week_of_month_3', 'week_of_month_4',
       'week_of_month_5', 'month_of_year_1', 'month_of_year_2',
       'month_of_year_3', 'month_of_year_4', 'month_of_year_5',
       'month_of_year_6', 'month_of_year_7', 'month_of_year_8',
       'month_of_year_9', 'month_of_year_10', 'month_of_year_11',
       'month_of_year_12']
    
    df['mean'] = df.CLIENT_OUT.rolling(window=7, center=False).mean()

    df['std'] = df.CLIENT_OUT.rolling(window=7, center=False).std()
    
    dfs = []
    
    for i in range(1, 6):
#         print(i)
        dfs.append(shift(df, i))
    
    for i in range(len(dfs)):
        dfs[i] = dfs[i].drop('mean', 1)
        dfs[i] = dfs[i].drop('std', 1)
#         dfs[i] = dfs[i].dropna(subset=dfs[i].columns.drop('CLIENT_OUT'))
    
    return dfs