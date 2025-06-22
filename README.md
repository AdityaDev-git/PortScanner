PortScanner.py is a Python-based tool for scanning network ports and grabbing service banners. It helps identify open ports, detect running services, and collect version information from a target IP address. The tool supports scanning common ports, single ports, or a custom port range, with results displayed in the console, logged to a file, and exported to a text file.


Features:
Port Scanning: Scan single ports, a range of ports, or a predefined list of common ports (e.g., HTTP, SSH, FTP).
Banner Grabbing: Retrieve service banners to identify software and versions running on open ports.
Multi-threading: Efficiently scan multiple ports concurrently with configurable thread limits.
Output Options: Results are displayed in the console, saved to a log file, and exported to a timestamped text file.
Configurable Timeout: Adjust the timeout for port scans and banner grabs.
Error Handling: Robust validation for IP addresses, port numbers, and error logging.


Requirements:
Python 3.6+
Standard libraries: socket, threading, time, logging, datetime
No external dependencies required


Installation:
Clone the repository
cd network-scanner
Ensure Python 3 is installed:python3 --version


Usage:
Run the script:
python3 NetworkScanner.py


Follow the prompts:

Enter the target IP address (e.g., 192.168.1.1).
Choose a scan option:
1: Scan common ports (FTP, SSH, HTTP, etc.).
2: Scan a single port.
3: Scan a range of ports.
Specify a timeout (default: 2 seconds).
Enter 'quit' to exit.


Output:

Console displays real-time results.
Log file (scan_YYYYMMDD_HHMMSS.log) records all actions and errors.
Text file (scan_results_IP_YYYYMMDD_HHMMSS.txt) contains a summary of results.


.................................................................................................................
Important Notes:

Legal Warning: Only scan systems you have explicit permission to scan. Unauthorized scanning may be illegal.
Performance: Adjust max_threads (default: 50) in the code for larger scans to balance speed and resource usage.
Timeout: Lower timeouts speed up scans but may miss slow-responding services.
Future Enhancements: Planned features include vulnerability detection, CSV export.
..................................................................................................................
