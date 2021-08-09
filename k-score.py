import pandas as pd
import numpy as np

# master_df = pd.read_csv("passenger-trips.csv", dtype=str)
master_df = pd.read_csv(
    "passenger-trips.csv",
    dtype={"Sex": str, "Zip": str},
    parse_dates=["Pickup", "Dropoff", "DOB"],
)
print(master_df.head(3))
master_df.info()

print("Master Dataset size = ", len(master_df))


def gps_reduce(gps_df):
    for dp in range(5):
        gps_reduced = gps_df.round(decimals=dp)
        yield dp, gps_reduced


def create_k_anon_matrix(df, transform, k_anon_values):

    k_anon_matrix = pd.DataFrame({}, columns=k_anon_values)
    print(k_anon_matrix)

    for row_name, gps_reduced in transform(df):
        print("\n------------------------\n")
        print(gps_reduced)
        frequencies = gps_reduced.value_counts(ascending=True)
        k_result_values = {}

        for k in k_anon_values:
            match = frequencies[frequencies >= k].sum()
            total = frequencies.sum()
            print(match, " / ", total)
            result = round(match / total * 100, 2)
            k_result_values[k] = result

        row = pd.Series(k_result_values)
        row.name = row_name
        k_anon_matrix = k_anon_matrix.append(row)
        print(k_anon_matrix)

    k_anon_matrix.style.set_caption(
        "K-Anonymity Sensitivity Analysis: x=k, y=data precision"
    )
    return k_anon_matrix


k_anon_values = [1, 2, 5, 10, 20]
gps_loc = master_df[["Pickup_long", "Pickup_lat", "Dropoff_long", "Dropoff_lat"]].copy()
result = create_k_anon_matrix(gps_loc, gps_reduce, k_anon_values)
print(result)

exit()

df = pd.DataFrame(
    np.random.randint(0, 2, (10, 5)),
    columns=["Pickup_long", "Pickup_lat", "A", "B", "C"],
)
print(df)


def hardcode_setNaN(df, freq_cols, threshold):
    frequencies = df[freq_cols].value_counts()
    print(frequencies)
    condition = frequencies < threshold  # you can define it however you want
    mask_obs = frequencies[condition].index
    (a_vals, b_vals) = zip(*mask_obs)

    index = df.loc[df["A"].isin(a_vals) & df["B"].isin(b_vals)].index
    df.loc[index, ~df.columns.isin(freq_cols)] = np.nan


freq_cols = ["Pickup_long", "Pickup_lat"]
threshold = 5

hardcode_setNaN(df, freq_cols, threshold)
print(df)

import functools


def setNaN(df, freq_cols, threshold):
    frequencies = df[freq_cols].value_counts()
    print(frequencies)
    condition = frequencies < threshold  # you can define it however you want
    mask_obs = frequencies[condition].index
    (a_vals, b_vals, c_vals) = zip(*mask_obs)
    vals = zip(*mask_obs)

    zip_iterator = zip(freq_cols, vals)

    cond_dict = dict(zip_iterator)

    test = df["Pickup_long"].isin(a_vals)

    cond_list = []
    for key, values in cond_dict.items():
        cond_list.append(df[[key]].isin(values))
    all_conds = functools.reduce(lambda x, y: x & y, cond_list)

    idx = df.loc(all_conds).index

    index = df.loc[df["A"].isin(a_vals) & df["B"].isin(b_vals)].index
    df.loc[index, ~df.columns.isin(freq_cols)] = np.nan


def mask(df, size, columns):

    if (size > len(df)) or (size <= 0):
        size = len(df)
        print("\n-----------------------\n")
        print("Invalid size passed, size set to maximum: ", size)
        print("\n-----------------------\n")

    subset_df = df.head(size)[columns]
    for column in columns:
        mask_size = mask_dictionary[column]
        mask = ""
        for _ in range(mask_size):
            mask += "*"
        masked_column = subset_df[column].apply(
            lambda s: (s[0 : len(s) - mask_size] + mask)
            if mask_size <= len(s)
            else mask[: len(s)]
        )
        subset_df[column] = masked_column

    return subset_df


def analyse_table_k_anon(df, values=False):

    print("\n-----------------------\n")
    print("Dataset K-Anon Analysis\n")
    print("\n-----------------------\n")

    print("Dataset Information\n")
    df.info()
    print("\n-----------------------\n")
    print("Dataset size = ", len(df))
    print("\n-----------------------\n")

    print("K-Anonymity Min to Max Values\n")
    groupings = df.value_counts(ascending=True)
    if values:
        print(groupings.values)
    else:
        print(groupings)

    print("\n-----------------------\n")
    print(
        "\nOverall K-Anonymity Classification for dataset = ", groupings.values[0], "\n"
    )
    print("\n-----------------------\n")


master_df = pd.read_csv("passenger-trips.csv", dtype=str)
print(master_df.head(3))

print("Master Dataset size = ", len(master_df))

tmp = master_df.copy()

threshold = 5  # Remove items less than or equal to threshold

vc = tmp[["Pickup_long", "Pickup_lat"]].value_counts()
vals_to_remove = vc[vc <= threshold].index.values
tmp["Pickup"].loc[tmp["Pickup"].isin(vals_to_remove)] = np.nan

print(tmp)

analyse_table_k_anon(master_df)

dataset_size = 1000

include_columns = ["Zip"]

mask_dictionary = {
    "Pickup": 0,
    "Dropoff": 0,
    "Pickup_long": 0,
    "Pickup_lat": 0,
    "Dropoff_long": 0,
    "Dropoff_lat": 0,
    "Sex": 0,
    "Zip": 2,
    "DOB": 6,
}

reduced_df = mask(master_df, dataset_size, include_columns)
analyse_table_k_anon(reduced_df)


print(master_df["Pickup_long"].value_counts(ascending=True))

# x.name not in ['C', 'D', 'E', 'F'] from x.name!='C'
# master_df.apply(
#    lambda x: x.mask(x.map(x.value_counts()) < 2, "redacted") if x.name != "C" else x
# )

import matplotlib.pyplot as plt


def k_anon_bar_chart(df):
    rows = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    k_values = []
    for x in rows:
        x_dataset = df.head(x * 10000)
        print(len(x_dataset))
        matches = x_dataset.value_counts(ascending=True)
        print(matches)
        k_values.append(matches.values[0])

    title = df.iloc[1]
    title = "K-Anon With Masking: " + " ".join(title.values)

    colors = []
    for value in k_values:  # keys are the names of the boys
        if value < 5:
            colors.append("r")
        else:
            colors.append("g")

    plt.bar(rows, k_values, color=colors)
    for i in rows:
        plt.text(i, k_values[i - 1], k_values[i - 1], ha="center")
    plt.title(title)
    plt.xlabel("No of rows x 10,000")
    plt.xticks(rows)
    plt.ylabel("K-Anonymity Value")
    plt.show()


pseudo_pii = master_df[["Zip", "DOB", "Sex"]].copy()
pseudo_pii["DOB"] = pseudo_pii["DOB"].str[:3] + "0's"
pseudo_pii["Zip"] = pseudo_pii["Zip"].str[:3] + "**"
k_anon_bar_chart(pseudo_pii)


exit()


col = "Pickup_long"  # 'bar'
n = 3  # 2
tmp = master_df[master_df.groupby(col)[col].transform("count").ge(n)]
print(tmp[col].value_counts(ascending=True))

dataset_size = 97950

include_columns = ["Zip", "Sex", "DOB"]

mask_dictionary = {
    "Pickup": 0,
    "Dropoff": 0,
    "Pickup_long": 0,
    "Pickup_lat": 0,
    "Dropoff_long": 0,
    "Dropoff_lat": 0,
    "Sex": 0,
    "Zip": 2,
    "DOB": 6,
}

analyse_table_k_anon(master_df)

# plot
import matplotlib.pyplot as plt

dataset_size = 97950

include_columns = ["Zip", "Sex", "DOB"]

mask_dictionary = {
    "Pickup": 0,
    "Dropoff": 0,
    "Pickup_long": 0,
    "Pickup_lat": 0,
    "Dropoff_long": 0,
    "Dropoff_lat": 0,
    "Sex": 0,
    "Zip": 2,
    "DOB": 6,
}

masked_data = analyse_table_k_anon(master_df, dataset_size, include_columns)

exit()

sub_dataset = master_df.head(dataset_size)
masked_zips = mask(sub_dataset, "Zip", ZIP_MASK_LENGTH)
print("Sub Dataset size = ", len(sub_dataset))
print(masked_zips.value_counts(ascending=True))


print(masked_zips.head(10))

print(master_df["DOB"].value_counts(ascending=True))
print(master_df["Zip"].value_counts(ascending=True))
print(master_df["Sex"].value_counts(ascending=True))


df = pd.read_csv("data.csv", dtype=str)

print(df.head(10))

new_df = df[["Name", "Zip"]]
print(new_df)

freq = new_df.value_counts(ascending=True)
freq.to_csv("result.csv")
print(freq.tail(10))

k_score = freq.array[0].item()

print("K-Anonymity Score = ", k_score)

name = df["Name"].apply(lambda x: x.ljust(8, "*")[:8])

name_mask = pd.DataFrame()

for x in range(7, 0, -1):
    col_name = "name-" + str(x)
    name_mask[col_name] = name.apply(lambda n: n[:x].ljust(8, "*"))
    print(name_mask[col_name].value_counts())
