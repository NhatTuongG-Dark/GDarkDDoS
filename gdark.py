import threading
import requests

url = input('Enter URL: ')

def http_request():
    try:
        response = requests.get(url)
        print('HTTP Response Status Code:', response.status_code)
    except requests.RequestException as e:
        print(f'HTTP request failed with exception: {str(e)}')

def socket_request():
    try:
        import socket
        from urllib.parse import urlparse
        
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or 80  # Default to port 80 if not specified in the URL
        path = parsed_url.path or '/'
        
        with socket.create_connection((host, port)) as sock:
            request = f'GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n'
            sock.sendall(request.encode())
            response = sock.recv(1024)
        
        print('Socket Response:', response.decode('utf-8'))
    except Exception as e:
        print(f'Socket request failed with exception: {str(e)}')

# Perform requests simultaneously
threads = []
threads.append(threading.Thread(target=http_request))
threads.append(threading.Thread(target=socket_request))

for t in threads:
    t.start()

for t in threads:
    t.join()
