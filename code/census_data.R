if(!require(pacman)) install.packages('pacman')
pacman::p_load(tidycensus, dplyr, tigris, sf, here)
setwd(here())

juris_vars <- c("Median Gross Rent" = "B25064_001E", 
  "Median Home Value" = "B25077_001E")

metro_vars <- c("Median Household Income" = "B19013_001E")

## Download data for mapping ---------------------------------------------------
juris_data <- get_acs("place", juris_vars, year = 2021, state = "06"
  , geometry = TRUE)

metro_data <- get_acs("cbsa", metro_vars, year = 2021) 

ca_geo <- states() |> subset(GEOID == "06", select = c(GEOID, NAME))

ca_metro_geo <- core_based_statistical_areas(filter_by = ca_geo) |> 
  select(GEOID)

ca_metro_data <- merge(ca_metro_geo, metro_data, by = "GEOID")


## Tidy ------------------------------------------------------------------------
juris_data <- rename_with(juris_data, tolower) |> 
  mutate(name = gsub(", California", "", name),
    variable_label = factor(
      variable, 
      levels = gsub("E$", "", juris_vars), 
      labels = names(juris_vars)))

ca_geo <- rename_with(ca_geo, tolower)

ca_metro_data <- rename_with(ca_metro_data, tolower) |> 
  mutate(variable_label = factor(
    variable, 
    levels = gsub("E$", "", metro_vars), 
    labels = names(metro_vars)))

## save ------------------------------------------------------------------------

st_write(juris_data, "data/tidy/place_acs_data.gpkg")
st_write(ca_geo, "data/tidy/ca_shp.gpkg")
st_write(ca_metro_data, "data/tidy/metro_acs_data.gpkg")
