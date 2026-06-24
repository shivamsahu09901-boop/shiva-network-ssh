import os
import socket
import threading

LISTEN_PORT = int(os.environ.get("PORT", 8080))
TARGET_PORT = 2222 
BUFF_SIZE = 4096

def handle_client(client_socket):
    try:
        request = client_socket.recv(BUFF_SIZE).decode('utf-8', errors='ignore')
        if "upgrade: websocket" in request.lower():
            response = (
                "HTTP/1.1 101 <unknown><big><font color=\"red\">shivam boss switched protocol</font></big></unknown>\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n\r\n"
            )
            client_socket.sendall(response.encode())
            
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect(('127.0.0.1', TARGET_PORT))
            
            def forward(src, dst):
                try:
                    while True:
                        data = src.recv(BUFF_SIZE)
                        if not data: break
                        dst.sendall(data)
                except:
                    pass
                finally:
                    src.close()
                    dst.close()

            threading.Thread(target=forward, args=(client_socket, target_socket), daemon=True).start()
            threading.Thread(target=forward, args=(target_socket, client_socket), daemon=True).start()
        else:
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_socket.close()
    except Exception as e:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', LISTEN_PORT))
    server.listen(100)
    print(f"[*] Railway Cloud Proxy listening on port {LISTEN_PORT}...")
    
    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    main()

  
