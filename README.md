# Raspberry Pi Pico W Webserver

This project implements a simple web server program running on a Raspberry Pi Pico W microcontroller, allowing users to interact with it over Wi-Fi through a web interface.

## Features

- **Wi-Fi Connection**: Enables users to connect the Raspberry Pi Pico W to their local Wi-Fi network.
- **Web Interface**: Provides a web-based user interface for controlling and monitoring the microcontroller.
- **Login System**: Implements a basic login system to authenticate users and control access to certain features.
- **LED Toggle**: Demonstrates the functionality of toggling an LED on the Raspberry Pi Pico W through the web interface.

## Prerequisites

Before running the program, ensure you have the following:

- Raspberry Pi Pico W microcontroller
- Micro-USB cable
- Wi-Fi network with internet access
- Python development environment installed on your computer

## Getting Started

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Navigate to the Directory**: Move into the project directory.
3. **Install Dependencies**: Install the required Python dependencies using pip.
4. **Upload Files to Raspberry Pi Pico W**: Use Adafruit ampy to upload the Python files (`main.py`, `login.html`, `welcome.html`) to your Raspberry Pi Pico W.
5. **Connect to Wi-Fi**: Modify the `connect_wifi_manually()` function in `main.py` to connect to your Wi-Fi network. You can either manually enter your SSID and password or scan for available networks.
6. **Run the Program**: Safely eject the Raspberry Pi Pico W from your computer and power it on. The program will start running automatically.
7. **Access the Web Interface**: Once the Raspberry Pi Pico W is connected to your Wi-Fi network, you can access the web interface by entering its IP address in a web browser.

## Usage

- Open a web browser and navigate to the IP address of your Raspberry Pi Pico W.
- Follow the on-screen instructions to log in and interact with the microcontroller.
- Toggle the LED on/off or perform other actions available in the web interface.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to Adafruit for their contributions to the Raspberry Pi Pico ecosystem.
- Special thanks to the community for their support and feedback.
