import pandas as pd

# --------------------------------------------------------------
# 1. Define objective
# --------------------------------------------------------------

""" 
The objective of this script is to create a dataset of long term mirgant arrivals from India to New Zealand

"""

# --------------------------------------------------------------
# 2. Read raw data
# --------------------------------------------------------------

# Loading all the datasets using the provided format
india_raw_df = pd.read_csv(
    "../../data/raw/india_work_visa_20231212.csv", parse_dates=[0], index_col=[0], skiprows=1
).reset_index()

india_raw_df_statsnz = pd.read_csv(
    "../../data/raw/tourist arrival data  - india_arrivals.csv"
)


# --------------------------------------------------------------
# 3. Process data
# --------------------------------------------------------------

# Converting the month column to datetime with the day set to the first
# The format '%YM%m' matches your '2023M06' format and '01' sets the day to the first
india_raw_df_statsnz['Month'] = pd.to_datetime(india_raw_df_statsnz['month'] + '01', format='%YM%m%d')


# Resetting the index to make 'Month' a column
datasets = [
    india_raw_df_statsnz,
    india_raw_df,
]

# Merging all datasets on 'Month' column using pd.merge
merged_df = datasets[0]  # Initialize with the first dataset
for df in datasets[1:]:  # Iterate over the rest of the datasets
    merged_df = pd.merge(merged_df, df, on="Month", how="outer")


# Rename columns
rename_columns = {
    "New Zealand work visa: (India)": "India_visa_search",
}
merged_df.rename(columns=rename_columns, inplace=True)

merged_df.drop(['month'], axis=1, inplace=True)

# Setting 'Month' as the index
merged_df.set_index('Month', inplace=True)


# --------------------------------------------------------------
# Export
# --------------------------------------------------------------

merged_df.to_pickle("../../data/interim/merged_india_nz_arrivals_data.pkl")
