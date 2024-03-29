# Raspberry Pi Pico W Webserver : Thonny Software

This project implements a simple web server program running on a Raspberry Pi Pico W microcontroller, allowing users to interact with it over Wi-Fi through a web interface.

## Functionality Overview

### 1. Wi-Fi Connection
The `connect_wifi_manually()` function enables users to connect the Raspberry Pi Pico W to their local Wi-Fi network. Users have the option to either manually enter the SSID and password or scan for available networks.

### 2. HTTP Request Handling
The `handle_http_request(request)` function analyzes incoming HTTP requests and processes them according to their type (e.g., login page request, login process request, or welcome page request). It generates appropriate HTTP responses for each case.

### 3. Login System
- The `handle_login_page()` function generates the HTML for the login page, where users can enter their credentials.
- The `handle_login_process(request)` function manages the login process. It verifies the received user credentials and creates a session ID if the login is successful.

### 4. Web Interface
- The `handle_welcome_page(request)` function generates the HTML for the welcome page, which users access after successful login. 
- Users can interact with the microcontroller through the web interface, such as toggling an LED.

### 5. Cookie Management
The `extract_cookies(request)` function parses cookies from the request headers, facilitating easy cookie usage for session management.

### 6. Time Formatting
The `format_time_rfc1123(timestamp)` function formats time according to RFC 1123, which is used for setting cookie expiration.

### 7. Main Function
The `main()` function orchestrates the overall operation of the web server. It handles Wi-Fi connection, socket creation, incoming connection handling, request processing, and response sending.

## Usage

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python dependencies using pip.
4. Upload the Python files (`main.py`, `login.html`, `welcome.html`) to your Raspberry Pi Pico W using Adafruit ampy.
5. Modify the `connect_wifi_manually()` function in `main.py` to connect to your Wi-Fi network.
6. Power on the Raspberry Pi Pico W. The program will start running automatically.
7. Access the web interface by entering the Raspberry Pi Pico W's IP address in a web browser.
8. Log in and interact with the microcontroller through the web interface.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Adafruit for their contributions to the Raspberry Pi Pico ecosystem.
- Community for their support and feedback.
