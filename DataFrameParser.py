import pandas as pd # pandas voor dataframes
import re # regular expressions

# metrics log vinden
file_path = "C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\metrics_log2.txt"

# output directory voor csv files
output_dir = "C:\\Users\\Ok\\Desktop\\HoGent\\Project\\GraduaatsProef\\Data\\data2\\"

def parse_cpu_usage(lines): # functie om cpu usage te parsen
    cpu_usage = re.findall(r'(\d+\.\d+)', lines[2]) # alle decimale getallen vinden met regex 
    cpu_usage = [float(usage) for usage in cpu_usage]
    return {
        'cpu_user': cpu_usage[0],
        'cpu_system': cpu_usage[1],
        'cpu_nice': cpu_usage[2],
        'cpu_idle': cpu_usage[3],
        'cpu_wait': cpu_usage[4],
        'cpu_hardware_interrupt': cpu_usage[5],
        'cpu_software_interrupt': cpu_usage[6],
        'cpu_steal': cpu_usage[7]
    }

def parse_memory_usage(lines):
    mem_usage = re.findall(r'(\d+)', lines[6])
    swap_usage = re.findall(r'(\d+)', lines[7])
    mem_usage = [int(mem) for mem in mem_usage]
    swap_usage = [int(swap) for swap in swap_usage]
    return {
        'mem_total': mem_usage[0],
        'mem_used': mem_usage[1],
        'mem_free': mem_usage[2],
        'mem_shared': mem_usage[3],
        'mem_buff_cache': mem_usage[4],
        'mem_available': mem_usage[5],
        'swap_total': swap_usage[0],
        'swap_used': swap_usage[1],
        'swap_free': swap_usage[2]
    }

def parse_disk_io_section(lines, start_index, timestamp):
    headers = lines[start_index].split()
    disk_io_data = []
    i = start_index + 1

    while i < len(lines) and not lines[i].startswith('Time:'):
        values = lines[i].split()
        disk_io_metrics = dict(zip(headers, values))
        disk_io_metrics['timestamp'] = timestamp  
        disk_io_data.append(disk_io_metrics)
        i += 1

    return disk_io_data, i

def main(file_path, output_dir):
    with open(file_path, 'r') as file:
        content = file.readlines()

    timestamps = []
    cpu_data = []
    memory_data = []
    disk_io_all_data = []

    timestamp = None  

    i = 0
    while i < len(content):
        if content[i].startswith('Time:'):
            timestamp = pd.to_datetime(content[i].split('Time: ')[1].strip(), format='%Y-%m-%d %H:%M:%S')
            timestamps.append(timestamp)

            cpu_metrics = parse_cpu_usage(content[i:i + 4])
            memory_metrics = parse_memory_usage(content[i:i + 10])

            cpu_data.append(cpu_metrics)
            memory_data.append(memory_metrics)

            while not content[i].startswith('Device') and i < len(content):
                i += 1
            if i < len(content):
                disk_io_data, next_index = parse_disk_io_section(content, i, timestamp)  # Pass timestamp here
                disk_io_all_data.extend(disk_io_data)
                i = next_index 
        else:
            i += 1
    
    # Export naar DF
    cpu_df = pd.DataFrame(cpu_data, index=timestamps)
    memory_df = pd.DataFrame(memory_data, index=timestamps)
    disk_io_df = pd.DataFrame(disk_io_all_data)

    # Export naar CSV
    cpu_df.to_csv(output_dir + "cpu_data2.csv", index=True)
    memory_df.to_csv(output_dir + "memory_data2.csv", index=True)
    disk_io_df.to_csv(output_dir + "disk_io_data2.csv", index=False)

    print(f"Data exported to {output_dir}cpu_data.csv, {output_dir}memory_data.csv, and {output_dir}disk_io_data.csv")

if __name__ == "__main__":
    main(file_path, output_dir)
