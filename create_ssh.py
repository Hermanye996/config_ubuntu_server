#!/usr/bin/env python3
#
# Copyright (c) 2023 Herman Ye
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Herman Ye
# Description: This script will assist you in configuring SSH access
#   by obtaining the IP address of the server,
#   generating an SSH configuration,
#   and writing it to the SSH configuration file.
#
import socket
import os


def get_ip_address(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        # handle errors here
        return None


def configure_ssh(local_name, hostname, ip_address, private_key):
    config_path = os.path.expanduser("~/.ssh/config")
    config = f"""
Host {local_name}
    HostName {ip_address}
    User {hostname}
    IdentityFile {private_key}
    ForwardX11 yes
    """
    with open(config_path, "a") as f:
        f.write(config)
    print(f"Configured SSH for host {hostname}.")
    print(f"run 'ssh {local_name}' to SSH to your server.")


def main():
    # Get the private key path
    print(
        "The key is saved as ~/.ssh/private.key by default, \
enter empty to skip."
    )
    private_key = input("Copy your ssh private key path here: ")
    if not private_key:
        private_key = "~/.ssh/private.key"
        print(
            f"You entered empty, the key is saved as {private_key} by default")
    # Get the hostname
    hostname = input("Enter your Hostname of server: ")
    # Get the ip address
    ip_address = get_ip_address(hostname)
    # Get the local name of server
    print("You can access the server through 'ssh nick_name.'")
    local_name = input("Enter your nick name of server: ")
    # Configure SSH
    if ip_address:
        print(f"The IP address of {hostname} is {ip_address}")
        configure_ssh(local_name, hostname, ip_address, private_key)
    else:
        print(f"Could not resolve the IP address of {hostname}")


if __name__ == "__main__":
    main()
