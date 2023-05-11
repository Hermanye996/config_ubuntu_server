![No Password SSH](https://img.shields.io/badge/No%20Password%20SSH-orange)
&nbsp;
![One Step Configuration](https://img.shields.io/badge/One%20Step%20Configuration-pink)
&nbsp;
[![Ubuntu VERSION](https://img.shields.io/badge/Ubuntu%20Server-22.04%20RPi-green)](https://ubuntu.com/)
&nbsp;
[![LICENSE](https://img.shields.io/badge/license-Apache--2.0-informational)](https://Hermanye996/config_ubuntu_server/blob/main/LICENSE)
&nbsp;

# Config Ubuntu Server
The config_ubuntu_server script allows for quick and easy configuration of an Ubuntu server on your Raspberry Pi system. It includes root privilege settings and SSH configuration without needing to manually fetch the IP.


Take the hassle out of configuring an Ubuntu server on your Raspberry Pi system with the "config_ubuntu_server" project. This handy tool simplifies the process with one-step configuration, including root privilege settings and SSH configuration without the need for manual IP fetching. It's ideal for both beginners and advanced users seeking a seamless setup experience. Plus, enjoy the added convenience of running SSH commands in one line and password-less access with Visual Studio Code's remote-SSH feature. Let "config_ubuntu_server" handle the configuration while you focus on your next big project!

## Installation
To install, clone the repository directly from GitHub by running the following command:
```bash
git clone https://github.com/Hermanye996/config_ubuntu_server.git
```

## Usage

### 1. Start Configuration
To initiate the configuration process, run the `start_configuration.py` script with `sudo` permissions. This script will check for root permissions, prompt for user input such as the system-boot path and wifi credentials, generate SSH keys, and create a cloud-init configuration.

```bash
# On your PC
sudo python3 start_configuration.py
```
You can download ubuntu 22.04 server for Raspberry Pi from [Ubuntu](https://ubuntu.com/download/raspberry-pi)

### 2. Create SSH Configuration
After the cloud-init process has finished, you can run the `create_ssh.py` script. This script will assist you in configuring SSH access by obtaining the IP address of the server, generating an SSH configuration, and writing it to the SSH configuration file.

```bash
# On your PC
python3 create_ssh.py
```
### 3. Run SSH
You can easily use ssh in a single command now. 

And you can also use remote-SSH in Visual Studio Code without entering a password!

```bash
# On your PC
ssh your_server_nick_name
```
### 4. Update Configuration (Optional)
If you change your wifi name or wifi password, you can simply re-run step 1 and step 2 to easily update your settings.

```bash
# On your PC
sudo python3 start_configuration.py
```
```bash
# On your PC
python3 create_ssh.py
```
If you find this project useful, please consider giving it a ⭐️ star on GitHub! Your support helps us improve the project and encourages further development. Don't forget to share it with your friends and colleagues who might find it beneficial. Thank you for your support!

## Contributing
Contributions are always welcome! If you have any ideas, suggestions, or issues, feel free to contribute. Before submitting a pull request, please ensure you've read our [contributing guidelines](CONTRIBUTING.md).

## License
This project is licensed under the Apache License, Version 2.0. For more information, see the [LICENSE](LICENSE) file.

```
Copyright 2023 Herman Ye
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.                             
```
