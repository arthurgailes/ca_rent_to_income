if(!require(pacman)) install.packages('pacman')
pacman::p_load(tidycensus, dplyr, tigris, sf, here, testthat)
setwd(here())

juris_vars <- c("median_gross_rent" = "B25064_001E", 
  "median_home_value" = "B25077_001E")

metro_vars <- c("median_hh_income_cbsa" = "B19013_001E")

## Download data for mapping ---------------------------------------------------
juris_data <- get_acs("place", juris_vars, year = 2021, state = "06"
  , geometry = TRUE, output = 'wide')

metro_data <- get_acs("cbsa", metro_vars, year = 2021, output = 'wide') 

ca_geo <- states() |> subset(GEOID == "06", select = c(GEOID, NAME))

ca_metro_geo <- core_based_statistical_areas(filter_by = ca_geo) |> 
  select(GEOID)

ca_metro_data <- merge(ca_metro_geo, metro_data, by = "GEOID")


## Tidy ------------------------------------------------------------------------
place_data <- rename_with(juris_data, tolower) |> 
  select(-ends_with("m")) |> 
  rename(place_id = geoid, place = name) |> 
  mutate(place = gsub(", California", "", place))

ca_geo <- rename_with(ca_geo, tolower)

ca_metro_data <- rename_with(ca_metro_data, tolower) |> 
  select(-ends_with("m")) |> 
  rename(cbsa = name, cbsa_id = geoid)

# join places to metro by their centroid
metro_place_data <- st_join(ca_metro_data, st_centroid(place_data), left = FALSE) |> 
  select(place_id, median_hh_income_cbsa) |> 
  st_drop_geometry()

expect_true(between(nrow(metro_place_data), nrow(ca_metro_data), nrow(juris_data)))

place_data <- inner_join(place_data, metro_place_data, by = "place_id") |> 
  mutate(home_inc_ratio = median_hh_income_cbsa / median_home_value,
    rent_inc_ratio = median_hh_income_cbsa / 12 / median_gross_rent)


## save ------------------------------------------------------------------------

st_write(juris_data, "data/tidy/place_acs_data.gpkg", delete_dsn = TRUE)
st_write(ca_geo, "data/tidy/ca_shp.gpkg", delete_dsn = TRUE)
st_write(ca_metro_data, "data/tidy/metro_acs_data.gpkg", delete_dsn = TRUE)


