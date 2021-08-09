import pandas as pd
import numpy as np
from pandas.core import indexing

# master_df = pd.read_csv("passenger-trips.csv", dtype=str)
master_df = pd.read_csv(
    "passenger-trips.csv",
    dtype={"Sex": str, "Zip": str},
    parse_dates=["Pickup", "Dropoff", "DOB"],
)
print(master_df.head(3))
master_df.info()

print("Master Dataset size = ", len(master_df))

df = pd.DataFrame(
    np.random.randint(0, 2, (10, 5)),
    columns=["Pickup_long", "Pickup_lat", "A", "B", "C"],
)
print(df)


def setMissing(master_df, df, freq_cols, threshold):

    new_master_df = master_df.copy()

    frequencies = df[freq_cols].value_counts()
    print(frequencies)
    condition = frequencies <= threshold  # you can define it however you want
    mask_obs = frequencies[condition].index
    print(len(mask_obs))

    for row in mask_obs:
        row_filter = {}
        for i, col in enumerate(freq_cols):
            row_filter[col] = row[i]

        idx = df.loc[(df[list(row_filter)] == pd.Series(row_filter)).all(axis=1)].index
        print(idx)

        new_master_df.loc[idx, df.columns.isin(freq_cols)] = np.nan

    print(new_master_df)

    return new_master_df


freq_cols = ["Pickup_long", "Pickup_lat", "Dropoff_long", "Dropoff_lat"]
threshold = 5

gps_reduced = master_df.copy()
gps_reduced[freq_cols] = gps_reduced[freq_cols].round(decimals=2)
new_master_df = setMissing(master_df, gps_reduced, freq_cols, threshold)
