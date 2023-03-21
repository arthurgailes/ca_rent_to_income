#' Download Census shapefiles
if(!require(pacman)) install.packages('pacman')
pacman::p_load(dplyr, tigris, sf, here, testthat)
setwd(here())

## Download data for mapping ---------------------------------------------------
ca_place_2010 <- places(state = 6, year = 2019)

ca_place_2010 <- ca_place_2010 |>
  st_transform(4326) |>
  transmute(place_2010_id = GEOID, place_name = NAMELSAD) |>
  arrange(place_2010_id)

ca_place_2020 <- places(state = 6)

ca_place_2020 <- ca_place_2020 |>
  st_transform(4326) |>
  transmute(place_2020_id = GEOID, place_name = NAMELSAD) |>
  arrange(place_2020_id)

cbsa <- core_based_statistical_areas(cb = TRUE)

cbsa_ca <- cbsa |>
  st_transform(4326) |>
  transmute(cbsa_2020_id = GEOID, cbsa_name = NAME) |>
  filter(grepl(", CA", cbsa_name)) |>
  arrange(cbsa_2020_id)

st_write(ca_place_2010, "data/tidy/ca_place_2010.gpkg", delete_dsn = TRUE)
st_write(ca_place_2020, "data/tidy/ca_place_2020.gpkg", delete_dsn = TRUE)
st_write(cbsa_ca, "data/tidy/ca_cbsa.gpkg", delete_dsn = TRUE)
