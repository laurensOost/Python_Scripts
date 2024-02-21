import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np

# CPU data laden voor VM1
vm1_cpu_df = pd.read_csv("C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data1\\cpu_data1.csv", index_col=0, parse_dates=True)

# CPU data laden voor VM2
vm2_cpu_df = pd.read_csv("C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data2\\cpu_data2.csv", index_col=0, parse_dates=True)

# Memory data laden voor VM1
vm1_memory_df = pd.read_csv("C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data1\\memory_data1.csv", index_col=0, parse_dates=True)

# Memory data laden voor VM2
vm2_memory_df = pd.read_csv("C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data2\\memory_data2.csv", index_col=0, parse_dates=True)

# Disk I/O data laden voor VM1
vm1_disk_io_df = pd.read_csv("C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data1\\disk_io_data1.csv", parse_dates=['timestamp'])

# Disk I/O data laden voor VM2
vm2_disk_io_df = pd.read_csv("C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data2\\disk_io_data2.csv", parse_dates=['timestamp'])

# Custom date formatter voor x-as
date_formatter = DateFormatter("%Y-%m-%d %H:%M:%S")

# Plot CPU voor beide VMs
plt.figure(figsize=(12, 6))
plt.plot(vm1_cpu_df.index, vm1_cpu_df['cpu_user'], label='VM1 CPU User', linestyle='-', marker='o')
plt.plot(vm2_cpu_df.index, vm2_cpu_df['cpu_user'], label='VM2 CPU User', linestyle='-', marker='s')
plt.title('Comparison of VM CPU Usage Over Time')
plt.xlabel('Time')
plt.ylabel('CPU Usage (%)')
plt.gca().xaxis.set_major_formatter(date_formatter) # custom date formatter gebruiken 
plt.xticks(rotation=45) # x-as labels roteren voor betere leesbaarheid
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot memory voor beide VMs
plt.figure(figsize=(12, 6))
plt.plot(vm1_memory_df.index, vm1_memory_df['mem_used'], label='VM1 Memory Used', linestyle='-', marker='o')
plt.plot(vm2_memory_df.index, vm2_memory_df['mem_used'], label='VM2 Memory Used', linestyle='-', marker='s')
plt.title('Comparison of VM Memory Usage Over Time')
plt.xlabel('Time')
plt.ylabel('Memory Used (MB)')
plt.gca().xaxis.set_major_formatter(date_formatter)  # Apply the custom date formatter
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot I/O metrics voor VM1
plt.figure(figsize=(12, 6))
plt.plot(vm1_disk_io_df['timestamp'], vm1_disk_io_df['r/s'], label='VM1 r/s', linestyle='-', marker='o')
plt.plot(vm1_disk_io_df['timestamp'], vm1_disk_io_df['w/s'], label='VM1 w/s', linestyle='-', marker='s')
plt.plot(vm1_disk_io_df['timestamp'], vm1_disk_io_df['%util'], label='VM1 %util', linestyle='-', marker='x')

# Plot I/O metrics voor VM2
vm2_disk_io_df['timestamp'] = pd.to_datetime(vm2_disk_io_df['timestamp'])
vm2_disk_io_df.set_index('timestamp', inplace=True)
vm2_sda_data = vm2_disk_io_df[vm2_disk_io_df['Device'] == 'sda']
plt.plot(vm2_sda_data.index, vm2_sda_data['%util'], label='VM2 %util', linestyle='-', marker='o')

plt.title('Comparison of VM Disk I/O Metrics Over Time')
plt.xlabel('Time')
plt.ylabel('Value')
plt.gca().xaxis.set_major_formatter(date_formatter)
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
