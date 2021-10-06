import pandas as pd
from typing import List

# data processing ------------------------------------------------------------------------------------------------------

def to_datetime(dt: pd.Series, format: str = '%Y-%m-%d %H:%M:%S') -> pd.Series:
    return pd.to_datetime(dt, format=format)

def round_columns(data: pd.DataFrame, columns: List[str] = [], decimals: int=3) -> pd.DataFrame:
    for col in columns:
        data[col] = data[col].round(decimals)
    return data

def create_dt(start: str, end: str, freq: str = '10 min') -> pd.DataFrame:
    dt = pd.date_range(start, end, freq=freq)
    return pd.DataFrame({'date_time' : dt})

def filter_timeseries(data: pd.DataFrame,
                      start: str,
                      end: str,
                      freq: str = '10 min',
                      on: str = 'date_time') -> pd.DataFrame:
    dt = create_dt(start, end, freq)
    return pd.merge(dt, data, left_on='date_time', right_on=on, how='left')