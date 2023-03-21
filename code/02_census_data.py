"""
Census data downloaded from data.census.gov

Place median home value table: B25077
  - Note: this is unused in favor of AEI AVM data

CBSA median income table: B19013

"""

import pandas as pd

b19013_names = pd.read_csv("data/raw/ACSDT5Y2021.B19013-Data.csv", nrows=1).columns
b19013 = pd.read_csv("data/raw/ACSDT5Y2021.B19013-Data.csv", header=None, skiprows=2, names=b19013_names)

b25077_names = pd.read_csv("data/raw/ACSDT5Y2021.B25077-Data.csv", nrows=1).columns
b25077 = pd.read_csv("data/raw/ACSDT5Y2021.B25077-Data.csv", header=None, skiprows=2, names=b25077_names)

## CBSA Median Income
b19013_ca = b19013[b19013["NAME"].str.contains(", CA")].copy()
cbsa_income = b19013_ca[["GEO_ID", "B19013_001E"]].copy()

cbsa_income = cbsa_income.rename(columns={"GEO_ID": "cbsa_2020_id", "B19013_001E": "median_income_2021",})

cbsa_income["cbsa_2020_id"] = cbsa_income["cbsa_2020_id"].str[-5:]

cbsa_income.to_csv("data/tidy/cbsa_income.csv", index=False)

## Place Median Home Value
place_home_value = b25077[["GEO_ID", "B25077_001E"]].copy()

place_home_value = place_home_value.rename(columns={"GEO_ID": "place_2020_id", "B25077_001E": "median_home_value_2021"})

place_home_value["place_2020_id"] = place_home_value["place_2020_id"].str[-7:]

place_home_value.to_csv("data/tidy/place_home_value.csv", index=False)