# WinIPShield

**WinIPShield** is a simple tool that helps protect your Windows PC by blocking malicious IPs sourced from the **Abuse.ch Feodo Tracker**. Inspired by the [PC Security Channel](https://www.youtube.com/watch?v=7UWFJGeix_E) and community feedback, this script has been enhanced to offer additional security features.

## Features
- **Fetches IP blocklist**: Automatically downloads the latest list of malicious IPs from the **Abuse.ch Feodo Tracker**.
- **Validates IPs**: Ensures that only valid IP addresses are processed, excluding headers or metadata.
- **Firewall integration**: Automatically adds rules to your Windows firewall to block harmful IPs.
- **Review list**: Creates a text file with the IPs to be blocked for your review before proceeding.
- **Admin check**: Ensures the script is run with administrator privileges for proper firewall rule modifications.

## Installation

1. **Ensure Python is installed**: This tool requires Python to run. If Python is not installed, download and install it from [here](https://www.python.org/downloads/).
   
2. **Install dependencies**:  
   Open your terminal (Command Prompt or PowerShell on Windows) and install the required `requests` module by running:
   
   ```bash
   pip install requests
   ```
## Usage

Step 1: Clone or Download the Script
If you are familiar with Git, clone the repository:

```bash
git clone https://github.com/tobiasGuta/WinIPShield.git
```

Step 2: Run the Script
Open Command Prompt or PowerShell as Administrator (right-click and select "Run as administrator").

Navigate to the directory where you downloaded or cloned the script. For example:

``` bash
cd C:\path\to\WinIPShield
```

Run the script using Python:

```bash
py WinIPShield.py
```

Step 3: Review the IP Blocklist
The script will download the latest IP blocklist from Abuse.ch, validate the IPs, and create a file named ip_blocklist_to_add.txt in the same directory.

Important: The IP addresses will only be listed inside this file, not in the console.

Example content of ip_blocklist_to_add.txt:

```bash
The following IP addresses will be added to the blocklist:
185.61.177.17
185.61.177.18
185.61.177.19
```

Open the ip_blocklist_to_add.txt file and review the IPs listed. Ensure these IP addresses are correct and that you're comfortable blocking them.

Step 4: Confirm and Add to Firewall
Once you've reviewed the list, the script will prompt you to confirm if you want to proceed with blocking the IPs.

Step 4: Confirm and Add to Firewall
Once you've reviewed the list, the script will prompt you to confirm if you want to proceed with blocking the IPs.
Example Output:
```bash
Fetching IP blocklist from Abuse.ch...
Validating IP addresses...
Creating review file: ip_blocklist_to_add.txt...
Review the list in 'ip_blocklist_to_add.txt'.
Are these IPs correct? (Y/N):
```

Type Y to proceed, or N to abort the process. If you type Y, the tool will automatically add the rules to your Windows firewall to block those IPs.

Step 5: Firewall Rules Added
Once the process is complete, you’ll see a confirmation message:

