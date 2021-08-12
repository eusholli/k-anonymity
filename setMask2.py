import pandas as pd
import numpy as np
import time

master_df = pd.read_csv(
    "passenger-trips.csv",
    dtype={"Sex": str, "Zip": str},
    parse_dates=["Pickup", "Dropoff", "DOB"],
)

print("Master Dataset size = ", len(master_df))


def setMask(master_df, df, freq_cols, threshold):

    new_master_df = master_df.copy()

    frequencies = df[freq_cols].value_counts()
    condition = frequencies <= threshold  # you can define it however you want
    mask_obs = frequencies[condition].index.to_frame()

    new_master_index = df.set_index(freq_cols).index
    mask_index = mask_obs.set_index(freq_cols).index
    new_master_df.loc[new_master_index.isin(mask_index), freq_cols] = np.nan
    print(new_master_df)
    return new_master_df


freq_cols = ["Pickup_long", "Pickup_lat", "Dropoff_long", "Dropoff_lat"]
threshold = 5

gps_reduced = master_df.copy()
gps_reduced[freq_cols] = gps_reduced[freq_cols].round(decimals=2)

start = time.time()
new_master_df = setMask(master_df, gps_reduced, freq_cols, threshold)
end = time.time()

print("Execution time = ", round((end - start), 2))
