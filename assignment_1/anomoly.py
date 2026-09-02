import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('./assignment_1/air_temperature_sea_ice.csv')

font = {'size'   : 20}

matplotlib.rc('font', **font)
    
x = data['Year'] + (data['Month'] - 1) / 12

plt.plot(x, data['Monthly_Anomaly'], label='Monthly Anomaly', color='orange', alpha=0.5)
plt.plot(x, data['Annual_Anomaly'], label='Yearly Anomaly')
plt.fill_between(x, data['Annual_Unc'] + data['Annual_Anomaly'], data['Annual_Anomaly'] - data['Annual_Unc'], alpha=0.5, label='95% Confidence Interval')
plt.fill_between(x, -10, 10, where=(1951 <= data['Year']) & (data['Year'] <= 1980), color='grey', alpha=0.2, label='Baseline Period (1951-1980)')
plt.xlabel('Year')
plt.ylabel('Temperature Anomaly (°C)')
plt.title('Yearly Temperature Anomaly')
plt.ylim(-1.2, 1.7)
plt.legend()
plt.grid()
plt.show()