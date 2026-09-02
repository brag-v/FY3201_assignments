import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = pd.read_csv("./assignment_1/air_temperature_sea_ice.csv")
data["date"] = pd.to_datetime(data[["Year", "Month"]].assign(day=15))
data = data.set_index("date").sort_index()
data = data.loc["1970":]

font = {"size": 20}
matplotlib.rc("font", **font)

fit_by_start_year = {}
for start_date in ["1990", "1980", "1970"]:
    r = data.loc[start_date:"2024-01-01"]

    time = (r["Year"] + r["Month"] / 12).to_numpy().reshape(-1, 1)
    y = r["Annual_Anomaly"].to_numpy()
    reg = LinearRegression().fit(time, y)

    fit_by_start_year[start_date] = (r.index, reg.predict(time))

    slope = reg.coef_[0]

    y_pred = reg.predict(time)
    residuals = y - y_pred

    n = len(y)
    sse = np.sum(residuals**2)

    se_slope = np.sqrt((sse / (n - 2)) / np.sum((time.ravel() - time.mean()) ** 2))

    print(f"{slope * 10:.3f} ± {se_slope * 10:.3f} °C / 10 yrs")


plt.plot(data.index, data["Annual_Anomaly"], label="Annual Anomaly")
for start_date, (time, fit) in reversed(fit_by_start_year.items()):
    plt.plot(time, fit, label=f"Linear fit for {start_date}-2024", linewidth=2)
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly (°C)")
plt.title("Linear trend in temperature")
plt.ylim(-1.2, 1.7)
plt.legend()
plt.grid()
plt.show()
