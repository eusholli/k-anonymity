import pandas as pd
import numpy as np

# new_master_df = pd.read_csv("passenger-trips.csv", dtype=str)
new_master_df = pd.read_csv(
    "cleaned-trips.csv",
    dtype={"Sex": str},
    parse_dates=["Pickup", "Dropoff", "DOB"],
)
print(new_master_df.head(3))
new_master_df.info()

print("Master Dataset size = ", len(new_master_df))


def l_diversity_analysis(df, columns):

    lowest_l = None

    print("-----------------------")
    print("Dataset L-Diversity Analysis")
    print("-----------------------")

    print("Dataset Information")
    df.info()
    print("-----------------------")
    print("Dataset size = ", len(df))
    print("-----------------------")

    for col in columns:
        freq = working_df[col].value_counts(ascending=True)
        print(freq)

        print("\n-----------------------")
        print("L-Diversity Min to Max Values: ", col)
        groupings = df.value_counts(ascending=True)

        if lowest_l == None:
            lowest_l = freq.values[0]
        elif lowest_l > freq.values[0]:
            lowest_l = freq.values[0]

    print("-----------------------")
    print("Overall L-Diversity for dataset = ", lowest_l)
    print("-----------------------")


working_df = pd.DataFrame(
    {
        "Pickup_gps": pd.Series([], dtype="object"),
        "Dropoff_gps": pd.Series([], dtype="object"),
    }
)

working_df["Pickup_gps"] = list(
    zip(new_master_df["Pickup_long"], new_master_df["Pickup_lat"])
)
working_df["Dropoff_gps"] = list(
    zip(new_master_df["Dropoff_long"], new_master_df["Dropoff_lat"])
)

l_diversity_analysis(working_df, ["Pickup_gps", "Dropoff_gps"])
