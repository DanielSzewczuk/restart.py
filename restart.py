import os
import sys
import time
import subprocess
from pathlib import Path

def find_first_python_file():
    for file in Path('.').iterdir():
        if file.suffix == '.py' and file != "restart.py":
            return file.name
    return None

def file_has_changed(filename, last_modification_time):
    current_modification_time = os.path.getmtime(filename)
    return current_modification_time != last_modification_time, current_modification_time

def restart_program_on_file_change(filename):
    last_modification_time = os.path.getmtime(filename)
    current_process = None

    while True:
        has_changed, last_modification_time = file_has_changed(filename, last_modification_time)
        if has_changed:
            if current_process and current_process.poll() is None:
                current_process.terminate()
                current_process.wait()

            print(f"\nPlik {filename} został zmieniony, restartuję program.")
            current_process = subprocess.Popen([sys.executable, filename], stdout=sys.stdout, stderr=sys.stderr)
        
        time.sleep(2)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_to_watch = sys.argv[1]
    else:
        file_to_watch = find_first_python_file()
        if not file_to_watch:
            print("Nie znaleziono żadnego pliku Python w bieżącym folderze.")
            sys.exit(1)

    print(f"Monitorowanie pliku: {file_to_watch}")
    restart_program_on_file_change(file_to_watch)
