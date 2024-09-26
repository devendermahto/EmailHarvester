"""
    This file is part of EmailHarvester
    Copyright (C) 2016 @maldevel
    https://github.com/maldevel/EmailHarvester
    
    EmailHarvester - A tool to retrieve Domain email addresses from Search Engines.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

    For more see the file 'LICENSE' for copying permission.
"""

import subprocess
import re
import socket

app_emailharvester = None

def search(domain, limit):
    try:
        # Resolve domain to IP address
        ip_address = socket.gethostbyname(domain)

        # Construct the nmap command to enumerate SMTP users
        command = [
            'nmap',
            '--script', 'smtp-enum-users',
            '-p25,465,587,2525',
            ip_address
        ]

        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout

        # Log the output for debugging
        #print(f"Nmap Output:\n{output}")

        # Check for specific error messages
        if "Couldn't find any accounts" in output:
            print(f"[-] No accounts found for domain {domain}.")
            return []
        if "Method RCPT returned a unhandled status code" in output:
            print(f"[-] RCPT command returned an unhandled status code for domain {domain}.")
            return []

        # Regex to find usernames under smtp-enum-users
        usernames = re.findall(r'\|\s+([a-zA-Z0-9._%+-]+)', output)

        # Construct emails from usernames
        emails = [f"{username}@{domain}" for username in usernames]

        # Log found emails
        if emails:
            print(f"[+] Extracted Emails: {emails}")
        else:
            print(f"[-] No emails extracted for domain {domain}.")

        return emails

    except subprocess.CalledProcessError as e:
        print(f"Error running nmap: {e}")
        return []
    except socket.gaierror:
        print(f"Error: Unable to resolve domain {domain}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

class Plugin:
    def __init__(self, app, conf):
        global app_emailharvester
        app.register_plugin('nmapenum', {'search': search})
        app_emailharvester = app