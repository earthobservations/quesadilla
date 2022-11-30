import pandas as pd
import pytest

from quesadilla import Homogenization, Timeseries


def test_homogenization_different_frequencies():
    store = [
        Timeseries("b", pd.DataFrame({
            "date": [pd.Timestamp("1970-01-01 00:00"), pd.Timestamp("1970-01-01 01:00"), pd.Timestamp("1970-01-01 02:00")],
            "value": [pd.NA] * 3
        })),
        Timeseries("a", pd.DataFrame({
            "date": [pd.Timestamp("1970-01-01"), pd.Timestamp("1970-01-02"), pd.Timestamp("1970-01-03")],
            "value": [pd.NA] * 3
        })),
        Timeseries("b", pd.DataFrame({
            "date": [pd.Timestamp("1970-01-01"), pd.Timestamp("1971-01-01"), pd.Timestamp("1972-01-01")],
            "value": [pd.NA] * 3
        }))
    ]
    with pytest.raises(ValueError):
        Homogenization(store)

def test_homogenization_align_ts():
    store = [
        Timeseries("b", pd.DataFrame({
            "date": [pd.Timestamp("1970-01-01 00:00"), pd.Timestamp("1970-01-01 01:00"),
                     pd.Timestamp("1970-01-01 02:00")],
            "value": [pd.NA] * 3
        })),
        Timeseries("a", pd.DataFrame({
            "date": [pd.Timestamp("1970-01-01 01:00"), pd.Timestamp("1970-01-01 02:00"),
                     pd.Timestamp("1970-01-01 03:00")],
            "value": [pd.NA] * 3
        })),
        Timeseries("b", pd.DataFrame({
            "date": [pd.Timestamp("1970-01-01 02:00"), pd.Timestamp("1970-01-01 03:00"),
                     pd.Timestamp("1970-01-01 04:00")],
            "value": [pd.NA] * 3
        }))
    ]

    store = Homogenization._align_timeseries(store, freq=3600)
    print(store[0].date)
    expected = pd.Series([pd.Timestamp("1970-01-01 00:00"), pd.Timestamp("1970-01-01 01:00"), pd.Timestamp("1970-01-01 02:00"), pd.Timestamp("1970-01-01 03:00"),
                     pd.Timestamp("1970-01-01 04:00")])

    assert all([ts.date.equals(expected) for ts in store])
