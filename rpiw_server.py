import usocket as socket
import network
import ubinascii
import utime
import urandom
import machine
from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
tim = Timer()

# Function to toggle the LED
def tick(timer):
    global led
    led.toggle()

# Initialize the timer to toggle the LED
tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)

# Function to read HTML file
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except OSError:
        return None
# Function to scan and display available Wi-Fi networks
def scan_wifi_networks():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    scan_count = 0  # Initialize scan count
    
    while scan_count < 3:  # Scan Wi-Fi networks three times
        available_networks = wlan.scan()
        
        print("Available Wi-Fi Networks (Scan {}):".format(scan_count + 1))
        print("---------------------------------------------------------------------------------------------------------")
        print("{:<30} {:<20} {:<15}".format("SSID", "BSSID", "Signal Strength"))
        print("---------------------------------------------------------------------------------------------------------")
        
        for network_info in available_networks:
            ssid = network_info[0].decode()
            bssid = ":".join("{:02x}".format(b) for b in network_info[1])
            signal_strength = network_info[3]
            print("{:<30} {:<20} {:<15}".format(ssid, bssid, signal_strength))
        
        scan_count += 1  # Increment scan count
        
        if scan_count < 3:  # Wait for 5 seconds between scans if not the last scan
            print("Waiting for 3-5 seconds before next scan...")
            utime.sleep(2.5)
            
def connect_wifi_manually():
    print("Test wlan connection ")
    print("***********************************************************************************************************")

    # Prompt the user to choose the action
    print("N: Exit the program ")
    print("Y: Scan for Wi-Fi networks first, then enter your Wi-Fi SSID and password to turn on the server ")
    print("O: Skip the Wi-Fi scan and directly enter your Wi-Fi SSID and password to turn on the server ")
    choice = input("Do you want to check the Wi-Fi network and open the official Raspberry Pi Pico W web server? (Y/N/O): ").strip().lower()

    if choice == 'n':
        print("Wi-Fi connection cancelled")
        return None, None  # Return None values for SSID and password
    elif choice == 'o':
        # Proceed to enter SSID and password directly
        attempts = 0  # Initialize attempts counter
        while attempts < 3:  # Allow maximum of 3 attempts
            ssid = input("Enter your WIFI SSID (2.4Ghz only): ")
            password = input("Enter your WIFI PASSWORD: ")
            
            # Check if SSID or password is empty or password length is less than 8 characters
            if not ssid or not password or len(password) < 8:
                print("SSID or password is empty or password length is less than 8 characters. Please enter valid credentials.")
                attempts += 1  # Increment attempts counter
            else:
                break  # Exit the loop if valid credentials are provided
        
        # If maximum attempts reached, exit the program
        if attempts == 3:
            print("Maximum attempts reached. Exiting program.")
            return None, None
        
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        
        while not wlan.isconnected():
            pass
        
        if not wlan.isconnected():
            print("Failed to connect to Wi-Fi. Please check your credentials.")
            return None, None
        
        print("WiFi connected:", wlan.ifconfig())
        return ssid, password
    elif choice == 'y':
        # Proceed to enter SSID if the user wants to connect
        scan_wifi_networks()
        while True:
            ssid = input("Enter your WIFI SSID (2.4Ghz only): ")
            if not ssid:
                print("SSID cannot be empty. Please enter a valid SSID.")
                continue
            
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            available_ssids = [w[0].decode() for w in wlan.scan()]
            if ssid not in available_ssids:
                print("SSID not found. Please enter a valid SSID.")
                continue
            
            break

        while True:
            attempts = 0  # Initialize attempts counter
            while attempts < 3:  # Allow maximum of 3 attempts
                password = input("Enter your WIFI PASSWORD: ")
                if not password or len(password) < 8:
                    print("Password is empty or password length is less than 8 characters. Please enter a valid password.")
                    attempts += 1  # Increment attempts counter
                else:
                    break  # Exit the loop if valid password is provided
            
            # If maximum attempts reached, exit the program
            if attempts == 3:
                print("Maximum attempts reached. Exiting program.")
                return None, None
            
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                pass
            
            if not wlan.isconnected():
                print("Invalid password. Please enter the correct password.")
                continue
                
            break
                
        print("WiFi connected:", wlan.ifconfig())
        return ssid, password
    else:
        print("Invalid choice. Please enter 'Y' to connect, 'N' to cancel, or 'O' to skip Wi-Fi scan and enter credentials directly.")
        return None, None  # Return None values for SSID and password

# Function to handle login page
def handle_login_page():
    login_page_html = read_file("login.html")
    if login_page_html is None:
        print("Failed to read login HTML file")
        return "HTTP/1.1 404 Not Found\n\n404 Not Found"
    else:
        return "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(login_page_html), login_page_html)

# Function to handle login process
def handle_login_process(request):
    global session_id
    
    post_data = request.split(b'\r\n\r\n')[1]
    print("Post data:", post_data)

    if not post_data:
        print("No POST data received")
        return "HTTP/1.1 400 Bad Request\n\n"

    post_parts = post_data.split(b'&')

    if len(post_parts) != 2:
        print("Invalid POST data format")
        return "HTTP/1.1 400 Bad Request\n\n"

    try:
        username = post_parts[0].split(b'=')[1]
        password = post_parts[1].split(b'=')[1]
        print("Username:", username)
        print("Password:", password)

        # Perform authentication
        if username == b"RPI_ID" and password == b"RPI_POI171149":
            # Create a unique session ID for the user
            session_id = ubinascii.hexlify(machine.unique_id()).decode()
            
            # Set the expiration time for the cookie (e.g., 1 hour from now)
            expiration = utime.time() + 3600  # 3600 seconds = 1 hour
            
            # Format the expiration time into the required format (RFC 1123)
            expiration_str = format_time_rfc1123(expiration)
            
            # Create the cookie string
            cookie = "session_id={}; Expires={}; Path=/".format(session_id, expiration_str)
            
            # Return the response with a redirect to the welcome page and the cookie
            return "HTTP/1.1 302 Found\nSet-Cookie: {}\nLocation: /welcome.html\n\n".format(cookie)
        else:
            # Incorrect username or password, redirect back to login page with error message
            return "HTTP/1.1 302 Found\nLocation: /login.html?error=incorrect\n\n"
    except IndexError:
        print("Invalid POST data format")
        return "HTTP/1.1 400 Bad Request\n\n"

# Function to extract and parse cookies from request headers
def extract_cookies(request):
    cookies = {}
    headers = request.split(b'\r\n')
    for header in headers:
        if b"Cookie:" in header:
            cookie_str = header.split(b': ')[1].decode()
            cookie_list = cookie_str.split('; ')
            for item in cookie_list:
                key, value = item.split('=')
                cookies[key] = value
    return cookies

def handle_welcome_page(request):
    welcome_page_html = read_file("welcome.html")
    if welcome_page_html is None:
        print("Failed to read welcome HTML file")
        return "HTTP/1.1 404 Not Found\n\n404 Not Found"
    else:
        # Extract and parse cookies from request
        cookies = extract_cookies(request)
        
        # Check if session ID exists in cookies
        if 'session_id' in cookies:
            session_id_cookie = cookies['session_id']
            # Here, you should compare the session ID with valid session IDs stored in your application
            # If the session ID is valid, return the welcome page
            # If the session ID is invalid, redirect to login page
            # For example:
            if session_id_cookie == session_id:
                return "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(welcome_page_html), welcome_page_html)
            else:
                # Redirect to login page if session ID is invalid
                redirect_response = "HTTP/1.1 302 Found\nLocation: /login.html\n\n"
                return redirect_response
        else:
            # Redirect to login page if no valid session ID found in cookies
            redirect_response = "HTTP/1.1 302 Found\nLocation: /login.html\n\n"
            return redirect_response

# Function to format time according to RFC 1123
def format_time_rfc1123(timestamp):
    weekday_abbr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Convert timestamp to UTC time
    utc_time = utime.gmtime(timestamp)
    
    # Extract date and time components
    year = utc_time[0]
    month = utc_time[1]
    day = utc_time[2]
    hour = utc_time[3]
    minute = utc_time[4]
    second = utc_time[5]
    weekday = utc_time[6]

    # Format the time string
    formatted_time = "{}, {:02d} {} {:04d} {:02d}:{:02d}:{:02d} GMT".format(
        weekday_abbr[weekday], day, month_abbr[month - 1], year, hour, minute, second)
    
    return formatted_time

# Function to handle HTTP requests
def handle_http_request(request):
    if b"GET /login.html HTTP/1.1" in request.split(b'\r\n')[0]:
        return handle_login_page()
    elif b"POST /login_process.php HTTP/1.1" in request.split(b'\r\n')[0]:
        return handle_login_process(request)
    elif b"GET /welcome.html HTTP/1.1" in request.split(b'\r\n')[0]:
        return handle_welcome_page(request)
    else:
        # Redirect to login page if no valid request is found
        redirect_response = "HTTP/1.1 302 Found\nLocation: /login.html\n\n"
        return redirect_response

# Main function to handle incoming connections
def main():
    # Connect to WiFi manually
    ssid, password = connect_wifi_manually()
    
    # Check if Wi-Fi connection is established
    if ssid is None or password is None:
        print("Exiting program as Wi-Fi connection is cancelled.")
        return
    
    # Create a socket object
    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = urandom.randint(1024, 65535)  # Random port number between 1024 and 65535
    socket_object.bind(('', port)) 
    socket_object.listen(5)  # Listen for incoming connections

    ip_addr = network.WLAN(network.STA_IF).ifconfig()[0]  # Get IP address
    print("***********************************************************************************************************")
    print("Listening on port %d..." % port)
    print("IP address:", ip_addr)
    print("URL: http://{}:{}".format(ip_addr, port))
    print("***********************************************************************************************************")

    # Open the server immediately
    while True:
        # Accept incoming connection
        conn, addr = socket_object.accept()
        print("Got a connection from %s" % str(addr))
        
        # Receive the request data
        request = conn.recv(1024)
        print("Request:")
        print(request)
        
        # Handle the HTTP request
        response = handle_http_request(request)
        
        # Send the HTTP response
        conn.send(response.encode())

        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()


