import requests
import csv
import subprocess
import sys
import os
import re

# Function to check if the script is run with admin privileges (for Windows)
def is_admin():
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

# Get the list of IPs from the Abuse CH website
response = requests.get(url, verify=True)
response.raise_for_status()  # Ensure the request was successful

# Regex pattern to validate an IPv4 address
ip_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')

# List to hold valid IPs
valid_ips = []

# Process the CSV file content
csv_reader = csv.reader(response.text.splitlines())
for row in csv_reader:
    # Skip comment lines (those that start with #) and rows with column headers
    if row and (row[0].startswith("#") or row[0] in ["first_seen_utc", "dst_port", "c2_status", "last_online", "malware"]):
        continue
    for ip in row:
        ip = ip.strip()
        # Validate if the IP address is valid
        if ip and ip != "dst_ip" and ip_pattern.match(ip):
            valid_ips.append(ip)
        else:
            # Log suspicious or malformed entries (non-IP)
            if ip and ip != "dst_ip":
                print(f"Suspicious entry found: {ip} (ignoring)")

# Check if any valid IPs were found
if not valid_ips:
    print("Error: No valid IP addresses found in the blocklist.")
    sys.exit(1)

# Create a text file with the IPs to be added to the blocklist for user review
with open('ip_blocklist_to_add.txt', 'w') as file:
    file.write("The following IP addresses will be added to the blocklist:\n")
    for ip in valid_ips:
        file.write(f"{ip}\n")

print("A text file 'ip_blocklist_to_add.txt' has been created with the IPs to block.")
print("Please review the file and confirm if they are correct.")

# Ask user for confirmation before proceeding
confirmation = input("Do you want to proceed with blocking these IPs? (Y/N): ").strip().lower()

if confirmation != "y":
    print("Operation cancelled.")
    sys.exit(1)

# Delete the existing firewall rule (if any)
rule = "netsh advfirewall firewall delete rule name='BadIP'"
subprocess.run(["Powershell", "-Command", rule])

# Add firewall rules to block each IP
for ip in valid_ips:
    print(f"Adding rule to block: {ip}")
    rule = f"netsh advfirewall firewall add rule name='BadIP' Dir=Out Action=Block RemoteIP={ip}"
    subprocess.run(["Powershell", "-Command", rule])

print("IP blocklist processing complete.")
