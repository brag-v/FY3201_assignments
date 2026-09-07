import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

temperature = (
    pd.read_csv("./assignment_1/air_temperature_sea_ice.csv")[
        ["Year", "Annual_Anomaly"]
    ]
    .set_index("Year")
    .sort_index()
    .rename(columns={"Annual_Anomaly": "Temperature Anomaly"})
    .groupby("Year")
    .mean()
)
print(temperature.head())

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
print(world_population.head())

# from https://gml.noaa.gov/ccgg/trends/
co2 = (
    pd.read_csv("./assignment_1/co2_annmean_mlo.csv")[["year", "mean"]]
    .rename(columns={"year": "Year", "mean": "co2 mole fraction (ppm)"})
    .groupby("Year")
    .mean()
)
print(co2.head())

# from https://gml.noaa.gov/ccgg/trends_ch4/
ch4 = (
    pd.read_csv("./assignment_1/ch4_annmean_gl.csv")[["year", "mean"]]
    .rename(columns={"year": "Year", "mean": "ch4 mole fraction (ppm)"})
    .set_index("Year")
    .sort_index()
)
print(ch4.head())

joined = (
    temperature.join(world_population, how="inner")
    .join(co2, how="inner")
    .join(ch4, how="inner")
)
print(joined.head())

corr = joined.corr()

sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)

plt.show()
