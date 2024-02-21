import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# eerste dataset 
cpu_data1 = pd.read_csv('C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data1\\cpu_data1.csv')

# parse de timestamp kolom en zet het als index voor de eerste dataset
cpu_data1['timestamp'] = pd.to_datetime(cpu_data1['timestamp'], format='%d/%m/%Y %H:%M')
cpu_data1.set_index('timestamp', inplace=True)

# tweede dataset
file_path_vm2 = 'C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data2\\cpu_data2.csv'
vm2_cpu_df = pd.read_csv(file_path_vm2, index_col=0, parse_dates=True)

# verzeker dat de index een datetime object is (indien nog niet geparsed)
vm2_cpu_df.index = pd.to_datetime(vm2_cpu_df.index)

# plot de cpu idle tijd voor beide datasets
plt.figure(figsize=(12, 6))

# plot voor eerste CPU
sns.lineplot(data=cpu_data1['cpu_idle'], label='CPU 1 Idle')

# plot voor tweede CPU
sns.lineplot(data=vm2_cpu_df['cpu_idle'], label='CPU 2 Idle')

plt.title('CPU Idle Time Over Time for CPU 1 and CPU 2')
plt.xlabel('Timestamp')
plt.ylabel('CPU Idle (%)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

print("CPU 1 Data Info:")
cpu_data1.info()
print("\nCPU 2 Data Info:")
vm2_cpu_df.info()

