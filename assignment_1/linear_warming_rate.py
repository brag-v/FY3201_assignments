import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = pd.read_csv("./assignment_1/air_temperature_sea_ice.csv")
data["date"] = pd.to_datetime(data[["Year", "Month"]].assign(day=15))
data = data.set_index("date").sort_index()

font = {'size'   : 20}
matplotlib.rc('font', **font)

r = data.loc["1998-01-01":"2024-01-01"]

time = np.arange(len(r)).reshape(-1, 1)
reg = LinearRegression().fit(
    time.reshape(-1, 1), r["Annual_Anomaly"].to_numpy()
)

fit = reg.predict(time.reshape(-1, 1))

plt.plot(r.index, r["Annual_Anomaly"], label="Annual Anomaly")
plt.plot(r.index, fit, label="Linear fit")
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly (°C)")
plt.title("Linear trend in temperature")
plt.ylim(-1.2, 1.7)
plt.legend()
plt.grid()
plt.show()
