import subprocess
import time
import datetime

def run_subprocess(command, log_file):
    return subprocess.Popen(command, shell=True, stdout=log_file, stderr=subprocess.STDOUT)

def get_timestamp():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def monitor_subprocesses(commands, log_files):
    processes = [run_subprocess(command, log_file) for command, log_file in zip(commands, log_files)]
    
    while True:
        for index, process in enumerate(processes):
            if process.poll() is not None:
                timestamp = get_timestamp()
                print(f"{timestamp} Subprocess {index + 1} terminated unexpectedly. Restarting...")
                processes[index] = run_subprocess(commands[index], log_files[index])
        
        # Adjust the monitoring interval as needed (e.g., 1 second)
        time.sleep(1)

if __name__ == "__main__":
    subprocess_commands = [
        "hackrf_sweep -B -f 250:2350 -w 100000 -l 8 -g 24 | ./HFone_process_binary2.py",  # Run hackrf-one script
        "rtl_power -g 28 -w hamming -f 541.78M:542.78M:1k -i 1 - | ./Kerberos_process_text.py"   # Run kerberos script
    ]

    log_files = [
        open("hackrf.log", "a"),
        open("kerberos.log", "a")
    ]

    try:
        monitor_subprocesses(subprocess_commands, log_files)
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    finally:
        for log_file in log_files:
            log_file.close()
