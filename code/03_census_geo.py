"""
  Download places and cbsas for California
"""

# Rewrite the commented code in python
# Path: code/03_census_geo.py

import pandas as pd
import geopandas as gpd
import numpy as np
import pygris

ca_place_2010 = pygris.places(state="06", year=2019)

ca_place_2010 = ca_place_2010.to_crs(4326)[["GEOID", "NAMELSAD", "geometry"]]\
  .rename(columns={"GEOID": "place_2010_id", "NAMELSAD": "place_name"})\
  .sort_values(by="place_2010_id")

ca_place_2020 = pygris.places(state="06")

ca_place_2020 = ca_place_2020.to_crs(4326)[["GEOID", "NAMELSAD", "geometry"]]\
  .rename(columns={"GEOID": "place_2020_id", "NAMELSAD": "place_name"})\
  .sort_values(by="place_2020_id")


cbsa = pygris.core_based_statistical_areas(cb=True)

cbsa_ca = cbsa.to_crs(4326)[["GEOID", "NAME", "geometry"]]\
  .rename(columns={"GEOID": "cbsa_2020_id", "NAME": "cbsa_name"})\
  .query("cbsa_name.str.contains(', CA')")\
  .sort_values(by="cbsa_2020_id")

ca_place_2010.to_file("data/tidy/ca_place_2010.gpkg", driver="GPKG")
ca_place_2020.to_file("data/tidy/ca_place_2020.gpkg", driver="GPKG")
cbsa_ca.to_file("data/tidy/ca_cbsa.gpkg", driver="GPKG")