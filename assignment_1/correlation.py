import pandas as pd
import matplotlib.pyplot as plt


temperature = pd.read_csv("./assignment_1/air_temperature_sea_ice.csv")

# from https://ourworldindata.org/grapher/population-unwpp?overlay=download-data
world_population = pd.read_csv("./assignment_1/population-unwpp.csv")
world_population = (
    world_population.loc[world_population["Entity"] == "World"][
        ["Year", "Population (historical estimates)"]
    ]
    .set_index("Year")
    .sort_index()
    .rename(columns={"Population (historical estimates)": "Population"})
)

# from https://gml.noaa.gov/ccgg/trends/ 
co2 = pd.read_csv("./assignment_1/co2_trend_gl.csv")
print(co2.head())

# from https://gml.noaa.gov/ccgg/trends_ch4/ 
ch4 = pd.read_csv("./assignment_1/ch4_annmean_gl.csv")
print(ch4.head())
