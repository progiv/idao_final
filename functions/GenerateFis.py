import numpy as np 
import pandas as pd



def GenerateFis(df):
    def split(data):
        return [data[-7:], data[-14:-7], data[-21:-14], data[-28:-21], data[-34:-29]]

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
    
    def shift(df, i):
        df2 = df.copy()
        for n in [1,2,3,4,5]:
            N = n + 5 - i 
            df2['out_{}_weeks_ago'.format(N)] = df.CLIENT_OUT.shift(7*N)
            df2['out_{}_weeks_ago_plus_day'.format(N)] = df.CLIENT_OUT.shift(7*N-1)
            df2['out_{}_weeks_ago_minus_day'.format(N)] = df.CLIENT_OUT.shift(7*N+1)
        return df2
    
    df['month_of_year'] = df.DATE.dt.month
    df['day_of_week'] = df.DATE.dt.dayofweek
    df['day_of_month'] = df.DATE.dt.day
    df['week_of_month'] = (df.DATE.dt.day  - 1) // 7 + 1
    df['holiday_dummy'] = holiday(df)
    
    list_dummies = ['day_of_week', 
                'day_of_month',
                'week_of_month',
                'month_of_year']
    df = pd.get_dummies(df, columns=list_dummies)
    
    df_splitted = []
    for i in range(1, 5):
        df_splitted.append(shift(df, i))
    
    return df_splitted