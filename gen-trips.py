import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(4321)

# df = pd.read_csv('trips.csv', dtype=str, nrows=1000)
df = pd.read_csv("trips.csv")

df.drop(
    columns=[
        "VendorID",
        "passenger_count",
        "trip_distance",
        "RateCodeID",
        "store_and_fwd_flag",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "improvement_surcharge",
        "total_amount",
    ],
    inplace=True,
)

df.columns = [
    "Pickup",
    "Dropoff",
    "Pickup_long",
    "Pickup_lat",
    "Dropoff_long",
    "Dropoff_lat",
]

gender = []
zip_code = []
dob = []

# Get rid of bad 0 values
df.drop(df.index[df["Pickup_long"] == 0], inplace=True)
df.drop(df.index[df["Pickup_lat"] == 0], inplace=True)
df.drop(df.index[df["Dropoff_long"] == 0], inplace=True)
df.drop(df.index[df["Dropoff_lat"] == 0], inplace=True)

for x in range(0, len(df), 1):
    gender.append(fake.profile(fields=["sex"])["sex"])
    zip_code.append("10" + fake.postcode()[2:])
    dob.append(str(fake.date_of_birth(minimum_age=21, maximum_age=65)))

df["Sex"] = gender
# df["Zip"] = zip_code
df["DOB"] = dob

print(df.head(10))
df.info()

df.to_csv("passenger-trips.csv", index=False)

exit()

for (columnName, columnData) in df.iteritems():
    print("Colunm Name : ", columnName)
    max_len = len(columnData.values.max())
    print("Max Cell Length : ", max_len)
    df[columnName] = columnData.apply(lambda x: x.ljust(max_len, "*"))
