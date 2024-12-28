# WindowsIPBlocker

**WindowsIPBlocker** is a simple tool that helps protect your Windows PC by blocking malicious IPs sourced from the **Abuse.ch Feodo Tracker**. Inspired by the [PC Security Channel](https://www.youtube.com/watch?v=7UWFJGeix_E) and community feedback, this script has been enhanced to offer additional security features.

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
