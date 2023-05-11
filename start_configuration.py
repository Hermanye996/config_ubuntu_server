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
# Description: This script will check for root permissions,
#   prompt for user input such as the system-boot path and wifi credentials,
#   generate SSH keys, and create a cloud-init configuration.
#
import os
import shutil
import sys
import paramiko


def generate_ssh_keys():
    # Generate SSH key pair
    private_key = paramiko.RSAKey.generate(bits=2048)

    # Save private key locally
    private_key_file = "private.key"
    private_key.write_private_key_file(private_key_file)

    # Generate public key
    public_key = f"{private_key.get_name()} {private_key.get_base64()}"

    print(f"Private key saved as {private_key_file}")

    # Return public key to be written to SD card
    return public_key


def check_root_permissions():
    if os.geteuid() != 0:
        print("This script must be run as root.")
        print("Please run this script again with sudo.")
        sys.exit(1)


def main():
    # Check root permissions
    check_root_permissions()
    # Get user input
    print("1. Reinsert your SD card.")
    print("2. Run the 'lsblk' command to view the mount path of the SD card.")
    print("The mount path should look like '/media/your_PC_name/system-boot'")
    sd_boot_path = input("Enter the system-boot path to the SD card: ")
    # Check if the path is valid
    if sd_boot_path.endswith("system-boot"):
        print("Correct path. Continuing...")
    else:
        print("Invalid system-boot path. Please try again.")
        sys.exit(1)

    # Reset cloud-init if it exists
    writable_path = os.path.join(os.path.dirname(sd_boot_path), "writable")
    instance_path = os.path.join(writable_path, "var/lib/cloud/instances")
    if os.path.exists(instance_path):
        print(instance_path)
        print("cloud-init exists. Resetting cloud-init...")
        try:
            shutil.rmtree(instance_path)
        except Exception as e:
            print(f"Failed to delete {instance_path}: {e}")
            sys.exit(1)
    else:
        print(instance_path)
        print("cloud-init does not exist. Skipping reset...")

    ubuntu_password = input("Enter your new Ubuntu password: ")
    wifi_ssid = input("Enter your WiFi SSID: ")
    wifi_password = input("Enter your WiFi password: ")

    # Generate SSH keys
    public_key = generate_ssh_keys()
    private_key_file_path = os.path.abspath("private.key")

    print(f"Private key is saved at: {private_key_file_path}")
    # Get user home directory
    username = os.getenv('SUDO_USER')
    if username:
        user_home = f"/home/{username}"
        print(user_home)

    # Check if ssh directory exists
    ssh_dir = os.path.join(user_home, '.ssh')
    os.makedirs(ssh_dir, exist_ok=True)
    # Move private key to ~/.ssh
    destination_root = os.path.join(ssh_dir, 'private.key')
    try:
        shutil.copy2(private_key_file_path, destination_root)
        # Change permissions to 777 for access by ssh
        os.chmod(destination_root, 0o777)
        print(
            f"File {private_key_file_path} \
has been successfully moved to {destination_root}")
    except Exception as e:
        print(f"An error occurred while moving the private key file: {e}")

    # Create cloud-init configuration
    cloud_init_config = f"""#cloud-config
    ssh_pwauth: True
    chpasswd:
      list:
      - ubuntu:{ubuntu_password}
      - root:{ubuntu_password}
      expire: False

    users:
    - name: ubuntu
      ssh_authorized_keys: ["{public_key}"]
      sudo: ['ALL=(ALL) NOPASSWD:ALL']
      groups: sudo
      shell: /bin/bash

    - name: root
      ssh_authorized_keys: ["{public_key}"]
      sudo: ['ALL=(ALL) NOPASSWD:ALL']
      groups: sudo
      shell: /bin/bash

    write_files:
    - path: /etc/netplan/50-cloud-init.yaml
      content: |
        network:
          version: 2
          ethernets:
            eth0:
              dhcp4: true
              optional: true
          wifis:
            wlan0:
              dhcp4: yes
              optional: true
              access-points:
                "{wifi_ssid}":
                  password: "{wifi_password}"

    packages:
    - git

    runcmd:
    - netplan apply

    """
    with open(f"{sd_boot_path}/user-data", "w") as f:
        f.write(cloud_init_config)
    print("\n*********Configuration Complete*********")
    print("Please eject your SD card and insert it into your device.")
    print("Then run 'ip addr' on device \
to check if your device has WIFI ip address."
          )
    print(
        "If you wish to establish an ssh keyed connection, \
follow these steps:"
    )
    print("1. Start your server.")
    print("2. Wait a few minutes until cloud-init completes.")
    print("3. Run 'create_ssh.py'")
    print("*" * 40)


if __name__ == "__main__":
    main()
