# Spatial join CBSA income to place home value

import pandas as pd
import geopandas as gpd

place_avm = pd.read_csv("data/tidy/ca_place_avm.csv", dtype={"place_2010_id": str})
cbsa_income = pd.read_csv("data/tidy/cbsa_income.csv", dtype={"cbsa_2020_id": str})

place_geo = gpd.read_file("data/tidy/ca_place_2010.gpkg")
cbsa_geo = gpd.read_file("data/tidy/ca_cbsa.gpkg")

# create centroid version of place geometry
place_centroid = place_geo.copy()
place_centroid["geometry"] = place_centroid["geometry"].to_crs(3857).centroid.to_crs(4326)

# join each place centroid to cbsa
place_cbsa = gpd.sjoin(place_centroid, cbsa_geo, how="left", predicate="within")

# join cbsa code to each place
place_geo_data = place_geo.merge(place_cbsa[["place_2010_id", "cbsa_2020_id", "cbsa_name"]], on="place_2010_id")

# add cbsa median income to each place
place_geo_data = place_geo_data.merge(cbsa_income, on="cbsa_2020_id")
place_geo_data = place_geo_data.merge(place_avm, on="place_2010_id")

place_geo_data["avm_income_ratio"] = place_geo_data["avm_2021"] / place_geo_data["median_income_2021"]

place_geo_data.rename(columns={"median_income_2021": "cbsa_median_income_2021", "avm_2021": "place_median_avm_2021"}, inplace=True)

place_geo_data.to_file("data/tidy/map_data_income_avm.gpkg", driver="GPKG")