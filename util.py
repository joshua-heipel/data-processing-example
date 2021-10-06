import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from sklearn import linear_model
from sklearn.metrics import r2_score
import const

# quality control ------------------------------------------------------------------------------------------------------

def in_range(data: pd.Series, range: List[float]):
    return (data < range[0]) | (range[1] < data)

def max_change(data: pd.Series, max_diff: float) -> pd.Series:
    return ~(data.diff().abs() < max_diff)

def min_variability(data: pd.Series, min_diff: float, width: int) -> pd.Series:
    return ~(data.rolling(width).apply(func=lambda x: np.max(np.absolute(np.diff(x)))) > min_diff)

def max_light_intensity(data: pd.Series, max_intensity: float, width: int) -> pd.Series:
    return data.rolling(width, min_periods=1).apply(func=lambda x: np.sum(x > max_intensity)) > 0

def quality_control(data: pd.DataFrame) -> pd.DataFrame:

    data['qc1'] = in_range(data.temp, const.TEMP_RANGE)
    data['qc2'] = max_change(data.temp, const.MAX_TEMP_DIFF)
    data['qc3'] = min_variability(data.temp, const.MIN_TEMP_DIFF, 6)
    data['qc4'] = in_range(data.date_time.dt.hour, const.DAY_RANGE) & \
                  (max_light_intensity(data.temp, const.L1, 3) | max_light_intensity(data.temp, const.L2, 7))
    data['qc_total'] = data[['qc1', 'qc2', 'qc3', 'qc4']].any(1)

    return data

def hourly_mean(data: pd.DataFrame, variable: str = 'temp', flag: str = 'qc_total') -> pd.DataFrame:
    data = data.groupby(data.date_time.dt.floor('H')).agg({variable : 'mean', flag : 'any'})
    data.at[data[flag], variable] = np.NaN
    return data

# linear regression ----------------------------------------------------------------------------------------------------

def linear_regression(data: pd.DataFrame, x: str, y: str) -> Tuple[np.ndarray, float]:

    obs = data[[x, y]].dropna().to_numpy()
    X, Y = obs[:, 0, np.newaxis], obs[:, 1, np.newaxis]

    regr = linear_model.LinearRegression()
    regr.fit(X, Y)
    Y_hat = regr.predict(X)
    r2 =  r2_score(Y, Y_hat)

    pred = np.repeat(np.NaN, data.shape[0])
    pred[~data[x].isna()] = regr.predict(data[x].dropna().to_numpy()[:, np.newaxis])[:,0]

    return pred, r2

def regression_model(data: pd.DataFrame, references: List[str], variable: str) -> Tuple[pd.DataFrame, Dict[str, float]]:

    predictions = {}
    fit = {}
    for x in references:
        pred, r2 = linear_regression(data, x, variable)
        predictions[x] = pred
        fit[x] = r2

    predictions = pd.DataFrame(predictions)

    return predictions[sorted(fit, key=fit.get, reverse=True)], fit

def replace_na(data: pd.DataFrame, predictions: pd.DataFrame, variable: str) -> pd.DataFrame:

    for station in predictions:
        data[variable].fillna(predictions[station], inplace=True)
    return data