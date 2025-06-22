import socket
import threading
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename=f'scan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Common ports dictionary
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Alt"
}

# Store scan results for text export
scan_results = []

def grab_banner(ip, port, timeout=2):
    """Attempt to grab banner from open port"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        return banner if banner else "No banner received"
    except:
        return "Banner grab failed"

def scan_port(ip, port, timeout=2):
    """Scan a single port and attempt banner grab if open"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        
        if result == 0:
            banner = grab_banner(ip, port, timeout)
            service = COMMON_PORTS.get(port, "Unknown")
            output = f"Port {port} ({service}) is OPEN - Banner: {banner}"
            print(output)
            logging.info(output)
            scan_results.append(output)
        else:
            output = f"Port {port} is CLOSED"
            print(output)
            logging.info(output)
            scan_results.append(output)
        s.close()
    except Exception as e:
        output = f"Port {port} scan failed: {str(e)}"
        print(output)
        logging.error(output)
        scan_results.append(output)

def export_results(ip):
    """Export scan results to a text file"""
    filename = f'scan_results_{ip}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    try:
        with open(filename, 'w') as f:
            f.write(f"Network Scan Results for {ip}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n\n")
            for result in scan_results:
                f.write(result + "\n")
            f.write("\nScan completed.\n")
        print(f"\nResults exported to {filename}")
        logging.info(f"Results exported to {filename}")
    except Exception as e:
        print(f"Failed to export results: {str(e)}")
        logging.error(f"Export failed: {str(e)}")

def scan_range(ip, start_port, end_port, timeout=2, max_threads=50):
    """Scan a range of ports using multiple threads"""
    print(f"\nStarting scan on {ip} from port {start_port} to {end_port}")
    print(f"Timeout: {timeout}s, Max threads: {max_threads}")
    logging.info(f"Scan started on {ip} from port {start_port} to {end_port}")
    
    start_time = time.time()
    
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, timeout))
        threads.append(thread)
        thread.start()
        
        # Control number of active threads
        while len([t for t in threads if t.is_alive()]) >= max_threads:
            time.sleep(0.1)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    elapsed_time = time.time() - start_time
    output = f"\nScan completed in {elapsed_time:.2f} seconds"
    print(output)
    logging.info(output)
    scan_results.append(output)
    
    # Export results to text file
    export_results(ip)

def main():
    """Main function to handle user input and initiate scans"""
    print("=== Network Scanner Tool ===")
    
    while True:
        try:
            ip = input("\nEnter IP to scan (or 'quit' to exit): ")
            if ip.lower() == 'quit':
                break
                
            socket.inet_aton(ip)  # Validate IP address
            
            # Clear previous results
            scan_results.clear()
            
            print("\nScan options:")
            print("1. Scan common ports")
            print("2. Scan single port")
            print("3. Scan port range")
            choice = input("Select option (1-3): ")
            
            timeout = float(input("Enter timeout in seconds (default 2): ") or 2)
            
            if choice == "1":
                for port in COMMON_PORTS.keys():
                    scan_port(ip, port, timeout)
                export_results(ip)
            
            elif choice == "2":
                port = int(input("Enter port number: "))
                if 1 <= port <= 65535:
                    scan_port(ip, port, timeout)
                    export_results(ip)
                else:
                    print("Invalid port number (1-65535)")
            
            elif choice == "3":
                start_port = int(input("Enter start port: "))
                end_port = int(input("Enter end port: "))
                if 1 <= start_port <= end_port <= 65535:
                    scan_range(ip, start_port, end_port, timeout)
                else:
                    print("Invalid port range (1-65535)")
            
            else:
                print("Invalid choice")
                
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except socket.error:
            print("Invalid IP address.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()