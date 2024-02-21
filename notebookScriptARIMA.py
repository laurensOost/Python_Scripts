import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

def perform_adf_test(series): # Augmented Dickey-Fuller test
    result = adfuller(series.dropna()) 
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

def run_arima(series, order): # Autoregressive Integrated Moving Average
    model = ARIMA(series, order=order)
    results = model.fit()
    print(results.summary())
    return results

# laden en resamplen van de data voor VM1 en VM2
vm1_memory_df = pd.read_csv('/mnt/data/memory_data1.csv', parse_dates=['timestamp'], dayfirst=True)
vm1_resampled = vm1_memory_df.set_index('timestamp').resample('10T').mean().interpolate()

vm2_memory_df = pd.read_csv('/mnt/data/memory_data2.csv', parse_dates=['timestamp'], dayfirst=True)
vm2_resampled = vm2_memory_df.set_index('timestamp').resample('10T').mean().interpolate()

# ADF test en ARIMA voor VM1 en VM2
print("VM1 Memory Data:")
perform_adf_test(vm1_resampled['mem_used'])
vm1_arima_results = run_arima(vm1_resampled['mem_used'], order=(1, 0, 1))

print("\nVM2 Memory Data:")
perform_adf_test(vm2_resampled['mem_used'])
vm2_arima_results = run_arima(vm2_resampled['mem_used'], order=(1, 0, 1))

# Forecasting voor VM1 en VM2
vm1_forecast = vm1_arima_results.get_forecast(steps=144)  
vm1_forecast_index = pd.date_range(start=vm1_resampled.index[-1], periods=145, freq='10T')[1:]
vm1_forecast_mean = vm1_forecast.predicted_mean
vm1_conf_int = vm1_forecast.conf_int()

vm2_forecast = vm2_arima_results.get_forecast(steps=144)  
vm2_forecast_index = pd.date_range(start=vm2_resampled.index[-1], periods=145, freq='10T')[1:]
vm2_forecast_mean = vm2_forecast.predicted_mean
vm2_conf_int = vm2_forecast.conf_int()

# en hoppa naar de grafieken voor VM1 en VM2
plt.figure(figsize=(12, 6))
plt.plot(vm1_resampled.index, vm1_resampled['mem_used'], label='VM1 Memory Used')
plt.plot(vm1_forecast_index, vm1_forecast_mean, label='VM1 Forecast', color='red')
plt.fill_between(vm1_forecast_index, vm1_conf_int.iloc[:, 0], vm1_conf_int.iloc[:, 1], color='red', alpha=0.3)
plt.title('VM1 Memory Usage Forecast for the Next 24 Hours')
plt.xlabel('Time')
plt.ylabel('Memory Used (MB)')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(vm2_resampled.index, vm2_resampled['mem_used'], label='VM2 Memory Used')
plt.plot(vm2_forecast_index, vm2_forecast_mean, label='VM2 Forecast', color='red')
plt.fill_between(vm2_forecast_index, vm2_conf_int.iloc[:, 0], vm2_conf_int.iloc[:, 1], color='red', alpha=0.3)
plt.title('VM2 Memory Usage Forecast for the Next 24 Hours')
plt.xlabel('Time')
plt.ylabel('Memory Used (MB)')
plt.legend()
plt.show()
