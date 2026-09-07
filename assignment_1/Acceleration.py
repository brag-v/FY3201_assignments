import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Change DATASET to choose which column to use
DATASET = "Annual"
VALUE_COL = f"{DATASET}_Anomaly"
UNC_COL = f"{DATASET}_Unc"

data = pd.read_csv("./air_temperature_sea_ice.csv")

x = data["Year"] + (data["Month"] - 1) / 12

# Function to do a weighted linear fit and return the results
def weighted_linear_fit(x_vals, y_vals, y_unc):
    weights = 1 / (y_unc ** 2)
    coeffs, cov = np.polyfit(x_vals, y_vals, 1, w=weights, cov="unscaled")
    m, b = coeffs
    m_err = np.sqrt(cov[0, 0])
    b_err = np.sqrt(cov[1, 1])

    residuals = y_vals - (x_vals * m + b)
    chi2 = np.sum((residuals / y_unc) ** 2)
    dof = len(x_vals) - len(coeffs)
    chi2_red = chi2 / dof

    return {"x": x_vals, "m": m, "b": b, "m_err": m_err, "b_err": b_err, "chi2_red": chi2_red}



periods_1 = [(1850, 1879), (1880, 1909), (1910, 1939), (1940, 1969), (1970, 1999), (2000, 2025)]
risultati_1 = {}

for start, end in periods_1:
    mask = (data["Year"] >= start) & (data["Year"] <= end) & (data[VALUE_COL].notna())
    x_p = x[mask]
    y_p = data.loc[mask, VALUE_COL]
    y_unc_p = data.loc[mask, UNC_COL]/1.96

    fit = weighted_linear_fit(x_p, y_p, y_unc_p)
    risultati_1[(start, end)] = fit

    print(f"{start}-{end}: m = {fit['m']:.5f} +/- {fit['m_err']:.5f}, chi2 normalized = {fit['chi2_red']:.5f}")

print()

periods_2 = [(1865, 1894), (1895, 1924), (1925, 1954), (1955, 1984), (1985, 2014)]
risultati_2 = {}

for start, end in periods_2:
    mask = (data["Year"] >= start) & (data["Year"] <= end) & (data[VALUE_COL].notna())
    x_p = x[mask]
    y_p = data.loc[mask, VALUE_COL]
    y_unc_p = data.loc[mask, UNC_COL]/1.96

    fit = weighted_linear_fit(x_p, y_p, y_unc_p)
    risultati_2[(start, end)] = fit

    print(f"{start}-{end}: m = {fit['m']:.5f} +/- {fit['m_err']:.5f}, chi2 normalized = {fit['chi2_red']:.5f}")

#Quadratic fit
mask_quad = (data["Year"] >= 1970) & (data["Year"] <= 2025) & (data[VALUE_COL].notna())
x_quad = x[mask_quad]
y_quad = data.loc[mask_quad, VALUE_COL]
y_unc_quad = data.loc[mask_quad, UNC_COL]/1.96
weights_quad = 1 / (y_unc_quad ** 2)

coeffs, cov = np.polyfit(x_quad, y_quad, 2, w=weights_quad, cov="unscaled")
a, b_quad, c_quad = coeffs
a_err = np.sqrt(cov[0, 0])
b_quad_err = np.sqrt(cov[1, 1])
c_quad_err = np.sqrt(cov[2, 2])

quad_fit_values = a*(x_quad**2) + b_quad*x_quad + c_quad
residuals_quad = y_quad - quad_fit_values
chi2_quad = np.sum((residuals_quad / y_unc_quad) ** 2)
dof_quad = len(x_quad) - len(coeffs)
chi2_red_quad = chi2_quad / dof_quad

print(f"\nQuadratic fit (1970-2025):")
print(f"a = {a:.6f} +/- {a_err:.6f}")
print(f"b = {b_quad:.6f} +/- {b_quad_err:.6f}")
print(f"c = {c_quad:.6f} +/- {c_quad_err:.6f}")
print(f"chi2 normalized = {chi2_red_quad:.6f}")

#Plot of the two linear fit side by side
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

# Left side: period set 1
axes[0].plot(x, data[VALUE_COL], color="gray", alpha=0.5, label="Annual anomaly")
axes[0].fill_between(x, data[VALUE_COL] + data[UNC_COL], data[VALUE_COL] - data[UNC_COL], color="gray", alpha=0.15, label="Uncertainty")
for (start, end), fit in risultati_1.items():
    axes[0].plot(fit["x"], fit["m"] * fit["x"] + fit["b"], label=f"Linear fit {start}-{end}")
axes[0].set_xlabel("Year", fontsize=13)
axes[0].set_ylabel("Temperature (°C)", fontsize=13)
axes[0].set_title("Period set 1", fontsize=14)
axes[0].grid()
axes[0].legend(fontsize=9)

# Right side: period set 2
axes[1].plot(x, data[VALUE_COL], color="gray", alpha=0.5, label="Annual anomaly")
axes[1].fill_between(x, data[VALUE_COL] + data[UNC_COL], data[VALUE_COL] - data[UNC_COL], color="gray", alpha=0.15, label="Uncertainty")
for (start, end), fit in risultati_2.items():
    axes[1].plot(fit["x"], fit["m"] * fit["x"] + fit["b"], label=f"Linear fit {start}-{end}")
axes[1].set_xlabel("Year", fontsize=13)
axes[1].set_title("Period set 2", fontsize=14)
axes[1].grid()
axes[1].legend(fontsize=9)

fig.suptitle("Linear fits over two different period sets", fontsize=16)
fig.tight_layout()

#Plot of the quadratic fit
plt.figure(figsize=(10, 6))
plt.plot(x_quad, y_quad, color="gray", alpha=0.5, label="Annual anomaly")
plt.fill_between(x_quad, y_quad + y_unc_quad, y_quad - y_unc_quad, color="gray", alpha=0.15, label="Uncertainty")
plt.plot(x_quad, quad_fit_values, color="tab:red", label="Quadratic fit")
plt.xlabel("Year", fontsize=16)
plt.ylabel("Temperature (°C)", fontsize=16)
plt.title("Quadratic fit", fontsize=18)
plt.legend(fontsize=11)
plt.grid()
plt.tight_layout()

plt.show()
