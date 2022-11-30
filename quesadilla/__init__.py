from typing import List, Union, Optional

import numpy as np
import pandas as pd


class Timeseries:
    def __init__(self, station_id: str, df: pd.DataFrame):
        self.station_id = station_id
        df = df.loc[:, ["date", "value"]].astype({"date": "datetime64", "value": pd.Float64Dtype()})
        self.df = df

    @property
    def date(self) -> Union[pd.Series, List[pd.Timestamp]]:
        return self.df.date

    @property
    def value(self) -> pd.Series:
        return self.df.value


class Homogenization:
    def __init__(self, store: List[Timeseries]):
        freq = self._assure_frequency(store)
        store = self._align_timeseries(store, freq)
        self.store = store

    @staticmethod
    def _assure_frequency(store: List[Timeseries]):
        def _get_frequencies(series: pd.Series) -> Optional[np.array]:
            return (series[1:].reset_index(drop=True) - series[:-1].reset_index(drop=True)).unique().tolist()[0]
        freq = [
            _get_frequencies(ts.date)
            for ts in store
        ]
        if len(set(freq)) != 1:
            raise ValueError()
        return freq[0].seconds

    @staticmethod
    def _align_timeseries(store: List[Timeseries], freq: int):
        min_date = min(map(lambda ts: ts.date.min(), store))
        max_date = max(map(lambda ts: ts.date.max(), store))
        fdr = pd.DataFrame({"date": pd.date_range(min_date, max_date, freq=f"{freq}S", inclusive="both")})
        for i, ts in enumerate(store):
            ts.df = fdr.merge(ts.df, how="left", on="date")
        return store
