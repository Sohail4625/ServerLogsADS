import time
from logs_to_df import logs_to_df
import re
import datetime
import csv
def monitor_log_file(log_file):
    previous_file_size = 0
    with open("data.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        line_count = sum(1 for row in reader)
        previous_file_size = line_count
    try:
        with open(log_file, 'r') as f:
            f.seek(previous_file_size)
            lines = f.readlines()
            lines = lines[previous_file_size:]
            if lines:
                for line in lines:  
                    current_line = logs_to_df(line)
                    if current_line != None:
                        timestamp = current_line[2]
                        timestamp_real = datetime.datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
                        if(timestamp_real.hour==datetime.datetime.now().hour and timestamp_real.date() == datetime.datetime.now().date()):
                            break
                        with open("data.csv", 'a',newline='') as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow(current_line)
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")


