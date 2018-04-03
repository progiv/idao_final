from datetime import datetime, timedelta
"""
Usage:
train_df, test_df = split_month_test(df)
train_df, test_df = split_month_test(df, test_period_length_in_days, train_period_length_in_days)
train_period_length_in_days=0 means use maximum
"""
def split_month_test(df, test_days=30, train_days=-1, unuseddays_in_end=0):
    end_day = max(df.DATE) - timedelta(days=unuseddays_in_end)
    delimiter_day =  end_day - timedelta(days=test_days-1)
    if train_days == -1:
        train_days = 5000 # it must work))

    start_day = max(min(df.DATE), delimiter_day - timedelta(days=train_days))
    #print(df.DATE.between(start_day, delimiter_day))
    train = df[df.DATE.between(start_day, delimiter_day - timedelta(days=1))]
    test = df[df.DATE.between(delimiter_day, end_day)]
    return train, test