import subprocess # shell commands uitvoeren
import time
import random
import statistics
from datetime import datetime, timedelta

def get_system_metrics():
    cpu_usage = subprocess.getoutput("top -bn1 | grep 'Cpu(s)'")
    memory_usage = subprocess.getoutput("free -m")
    disk_io = subprocess.getoutput("iostat -dx")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metrics = f"Time: {current_time}\nCPU Usage:\n{cpu_usage}\n\nMemory Usage:\n{memory_usage}\n\nDisk I/O:\n{disk_io}\n\n" #f = format string 
    return metrics

def log_metrics_to_file(metrics, file_path):
    with open(file_path, "a") as file:
        file.write(metrics)

def perform_stress_test(duration_seconds=600, cpu_workers=4, vm_workers=2, vm_bytes='256M'): # default values, dynamisch getypt dus geen type meegeven
    print(f"Starting stress test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    stress_cmd = f"stress --cpu {cpu_workers} --vm {vm_workers} --vm-bytes {vm_bytes} --timeout {duration_seconds}"
    subprocess.run(stress_cmd, shell=True)
    print(f"Stress test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def perform_statistical_calculations(data_size=50000):
    print(f"Starting calculations at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    data = [random.uniform(100, 1000) for _ in range(data_size)]
    sorted_data = sorted(data)
    unique_elements = set(data)
    mean = statistics.mean(data)
    median = statistics.median(data)
    stdev = statistics.stdev(data)
    variance = statistics.variance(data)
    print(f"Calculations completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    metrics_log_file = "/home/DummyAdmin/metrics_log.txt"
    start_time = datetime.now()

    while datetime.now() - start_time < timedelta(days=1): 
        perform_stress_test()  # Run stress test

        # elke tien minuten metrics verzamelen
        for _ in range(12):  
            metrics = get_system_metrics()
            log_metrics_to_file(metrics, metrics_log_file)
            time.sleep(600)  

    print("Completed 1 day of data collection and stress testing.")

if __name__ == "__main__":
    main()
