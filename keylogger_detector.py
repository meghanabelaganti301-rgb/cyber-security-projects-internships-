import psutil
import time

# Suspicious keywords to check in process name or command line
SUSPICIOUS_KEYWORDS = [
    "keylog", "keylogger", "keystroke", "pynput", "keyboard", "pyhook"
]

# Safe list: Add any known safe Python scripts or tools here
SAFE_PROCESS_NAMES = [
    "keylogger_detector.py"
]

# Function to detect keyloggers
def detect_keylogger():
    detected = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'] or ''
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            process_info = name.lower() + " " + cmdline.lower()

            if any(keyword in process_info for keyword in SUSPICIOUS_KEYWORDS):
                if any(safe in cmdline for safe in SAFE_PROCESS_NAMES):
                    continue  # Skip known safe tools

                print("\n[ALERT] Suspicious process detected!")
                print(f"[PID]: {pid}")
                print(f"[Name]: {name}")
                print(f"[CMD ]: {cmdline}")

                try:
                    proc.kill()
                    print("[ACTION] Process terminated successfully.\n")
                except Exception as e:
                    print(f"[ERROR] Failed to terminate process: {e}\n")

                detected = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not detected:
        print("[INFO] No suspicious keylogger activity detected.")

def main():
    print("Keylogger Detector Started... Press Ctrl+C to stop.\n")
    try:
        while True:
            detect_keylogger()
            time.sleep(5)  # Scan every 5 seconds
    except KeyboardInterrupt:
        print("\nDetection stopped by user.")

if __name__ == "__main__":
    main()
