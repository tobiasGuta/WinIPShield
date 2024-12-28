import requests
import csv
import subprocess
import sys
import os
import re

# Function to check if the script is run with admin privileges
def is_admin():
    try:
        return os.geteuid() == 0  # For Linux/macOS, checks if effective user ID is 0 (root)
    except AttributeError:
        try:
            return bool(subprocess.check_output('net session', stderr=subprocess.STDOUT, shell=True))  # For Windows, checks if admin privileges
        except subprocess.CalledProcessError:
            return False

# Check if the script is run with admin privileges
if not is_admin():
    print("Error: This script needs to be run with administrator privileges.")
    sys.exit(1)

# URL of the IP blocklist
url = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"

# Get the list of IPs from the Abuse CH website (ensure HTTPS and validate content)
response = requests.get(url, verify=True)  # Always use HTTPS and enable certificate verification
response.raise_for_status()  # Raise an exception if the request failed (404, 500, etc.)

# Regex pattern to validate an IPv4 address
ip_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')  # Simple regex to check for basic IPv4 addresses

# List to hold valid IPs
valid_ips = []

# Process the CSV file content
csv_reader = csv.reader(response.text.splitlines())
for row in csv_reader:
    for ip in row:
        # Strip any leading/trailing whitespace
        ip = ip.strip()
        # Skip empty entries or headers (e.g., if it's not an IP)
        if ip and ip != "dst_ip" and ip_pattern.match(ip):
            valid_ips.append(ip)
        else:
            # Log suspicious or malformed entries
            if ip and ip != "dst_ip":
                print(f"Suspicious entry found: {ip} (ignoring)")

# Check if any valid IPs were found
if not valid_ips:
    print("Error: No valid IP addresses found in the blocklist.")
    sys.exit(1)

# Create a text file with the list of IPs to be blocked
with open('ip_blocklist_to_add.txt', 'w') as file:
    file.write("The following IP addresses will be added to the blocklist:\n")
    for ip in valid_ips:
        file.write(f"{ip}\n")

print("IP blocklist has been saved to 'ip_blocklist_to_add.txt'. Please review it.")

# Ask user to confirm if the list is correct
confirmation = input("Is the list correct? (Y/N): ").strip().upper()
if confirmation != 'Y':
    print("Aborted. No changes were made.")
    sys.exit(1)

# Delete the existing firewall rule
rule = "netsh advfirewall firewall delete rule name='BadIP'"
subprocess.run(["Powershell", "-Command", rule])

# Add firewall rules to block each IP
for ip in valid_ips:
    rule = f"netsh advfirewall firewall add rule name='BadIP' Dir=Out Action=Block RemoteIP={ip}"
    subprocess.run(["Powershell", "-Command", rule])

print("IP blocklist processing complete. The following IPs have been blocked.")
