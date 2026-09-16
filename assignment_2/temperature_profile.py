import pandas as pd
import matplotlib.pyplot as plt

STATION = "SN44640"
DATA_COL = "Minimumstemperatur (døgn)"

df = pd.read_csv(f"assignment_2/{STATION}_temperature.csv", sep=";")
df[DATA_COL] = pd.to_numeric(df[DATA_COL], errors="coerce") 
df["date"] = pd.to_datetime(df["Tid (norsk normaltid)"], format="%d.%m.%Y")
df["year"] = df["date"].dt.year
df["day_of_year"] = df["date"].dt.dayofyear

print(df.describe())
print(df["Middeltemperatur (døgn)"].unique())

fig, ax = plt.subplots(figsize=(14, 6))
ax.scatter(df["day_of_year"], df[DATA_COL], s=10, color="gray", alpha=0.5)
ax.set_xlabel("Day number")
ax.set_ylabel(DATA_COL)
ax.set_xlim(1, 366)
ax.set_ylim(-25, 35)
ax.set_title(f"({STATION}) {DATA_COL}")
ax.grid(alpha=0.25)
fig.tight_layout()
plt.show()
