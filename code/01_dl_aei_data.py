"""
  This is the code to process the original AEI home income data.
For reference only; it's no longer needed because the truncated california
data is included in the data/raw directory.

AVM Source: https://aeihousingcenter.org/public/data/wod/block_20211013.zip

Place-Block crosswalk source: https://mcdc.missouri.edu/applications/geocorr2018.html

To repeat, just download, unzip in data/raw and run this script.
"""

""" Uncomment to run
import pandas as pd
import geopandas as gpd

ca_block_data = gpd.read_file("data/raw/block_20211013/block_data_06_20211013.shp")

ca_block_avm = ca_block_data[["geoid", "p50__21"]].copy()

ca_block_avm.rename(columns={"p50__21": "avm_2021", "geoid": "block_2010"}, inplace=True)

#  write to csv
ca_block_avm.to_csv("data/raw/ca_block_avm.csv", index=False)

# join to places
xwalk_place_block_names = pd.read_csv("data/raw/geocorr_block_to_place.csv", nrows = 1).columns

xwalk_place_block = pd.read_csv(
  "data/raw/geocorr_block_to_place.csv",
  header = None,
  skiprows=2,
  names=xwalk_place_block_names,
  dtype={"county": str, "tract": str, "block": str, "placefp": str}
  )

# remove . from tract
xwalk_place_block["tract"] = xwalk_place_block["tract"].str.replace(".", "")

xwalk_place_block["block_2010"] = xwalk_place_block["county"] + xwalk_place_block["tract"] + xwalk_place_block["block"]

xwalk_place_block["place_2010"] = "06" + xwalk_place_block["placefp"]

# test to ensure no block_2010 is duplicated
assert xwalk_place_block["block_2010"].nunique() == xwalk_place_block.shape[0]

xwalk_clean = xwalk_place_block[["block_2010", "place_2010", "placenm"]].copy()

# join to avm
ca_block_avm_place = ca_block_avm.merge(xwalk_clean, on="block_2010", how="inner")

# get median avms
ca_place_avm = ca_block_avm_place.groupby(["place_2010", "placenm"])["avm_2021"].median().reset_index()

# drop NAs
ca_place_avm.dropna(inplace=True)

ca_place_avm["placenm"] = ca_place_avm["placenm"].str.replace(", CA", "")

ca_place_avm.to_csv("data/tidy/ca_place_avm.csv", index=False)
"""