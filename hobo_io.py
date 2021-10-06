import pandas as pd
from data_processing import to_datetime, round_columns

# io functions ---------------------------------------------------------------------------------------------------------

def read_raw_hobo(file: str) -> pd.DataFrame:
    data = pd.read_csv(file, skiprows=2, names=('date_time', 'temp', 'lux'), usecols=(1, 2, 3))
    data['date_time'] = to_datetime(data['date_time'], '%d/%m/%Y %H:%M:%S')
    return data

def write_10min_hobo(data: pd.DataFrame, file: str) -> None:
    data = round_columns(data, ['temp', 'lux'])
    data.to_csv(file, index=False)

def read_10min_hobo(file: str) -> pd.DataFrame:
    data = pd.read_csv(file)
    data['date_time'] = to_datetime(data['date_time'])
    return data

def read_reference(file: str) -> pd.DataFrame:
    data = pd.read_csv(file)
    data['date_time'] = to_datetime(data['date_time'])
    return data

def write_hourly_hobo(data: pd.DataFrame, file: str) -> None:
    data = round_columns(data, ['th'])
    data.to_csv(file, index=False)