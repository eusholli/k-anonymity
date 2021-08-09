import pandas as pd
import numpy as np

# master_df = pd.read_csv("passenger-trips.csv", dtype=str)
master_df = pd.read_csv(
    "passenger-trips.csv",
    dtype={"Sex": str},
    parse_dates=["Pickup", "Dropoff", "DOB"],
)
print(master_df.head(3))
master_df.info()

print("Master Dataset size = ", len(master_df))

pickup_columns = ["DOB", "Sex", "Pickup", "Pickup_long", "Pickup_lat"]
working_df = master_df[pickup_columns].copy()

working_df["DOB"] = master_df["DOB"].dt.year
working_df["Pickup"] = master_df["Pickup"].dt.hour
print(working_df.head(3))


def dob_reduce(df):
    def custom_round(x, base=5):
        return int(base * round(float(x) / base))

    for year_precision in [1, 5, 10]:
        df["DOB"] = df["DOB"].apply(lambda x: custom_round(x, base=year_precision))
        print(df)
        yield year_precision, df


# run analysis of data precision versus wanted k-anonymity value
def create_k_anon_matrix(df, transform, k_anon_values):

    k_anon_matrix = pd.DataFrame({}, columns=k_anon_values)

    for row_name, gps_reduced in transform(df):
        frequencies = gps_reduced.value_counts(ascending=True)
        k_result_values = {}

        for k in k_anon_values:
            match = frequencies[frequencies >= k].sum()
            total = frequencies.sum()
            result = round(match / total * 100, 2)
            k_result_values[k] = result

        row = pd.Series(k_result_values)
        row.name = row_name
        k_anon_matrix = k_anon_matrix.append(row)

    return k_anon_matrix


# Call the functions for analysis

print(working_df.head(3))
k_anon_values = [2, 5, 10, 50, 100, 1000]
result = create_k_anon_matrix(
    working_df[["DOB", "Sex", "Pickup"]].copy(), dob_reduce, k_anon_values
)

print(result)

print(working_df)
