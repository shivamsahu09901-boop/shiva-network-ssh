import os
import socket
import threading

LISTEN_PORT = int(os.environ.get("PORT", 8080))
TARGET_PORT = 2222 
BUFF_SIZE = 8192
TIMEOUT = 300

def handle_client(client_socket):
    try:
        client_socket.settimeout(TIMEOUT)
        request = client_socket.recv(BUFF_SIZE).decode('utf-8', errors='ignore')
        
        if "upgrade: websocket" in request.lower():
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n\r\n"
            )
            client_socket.sendall(response.encode())
            
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.settimeout(TIMEOUT)
            target_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            target_socket.connect(('127.0.0.1', TARGET_PORT))
            
            def forward(src, dst):
                try:
                    while True:
                        data = src.recv(BUFF_SIZE)
                        if not data: 
                            break
                        dst.sendall(data)
                except:
                    pass
                finally:
                    try:
                        src.close()
                        dst.close()
                    except:
                        pass

            t1 = threading.Thread(target=forward, args=(client_socket, target_socket), daemon=True)
            t2 = threading.Thread(target=forward, args=(target_socket, client_socket), daemon=True)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_socket.close()
    except Exception as e:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server.bind(('0.0.0.0', LISTEN_PORT))
    server.listen(200)
    print(f"[*] Proxy listening on port {LISTEN_PORT}...")
    
    while True:
        try:
            client_sock, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
    
