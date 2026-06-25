import os
import socket
import threading

LISTEN_PORT = int(os.environ.get("PORT", 8080))
TARGET_PORT = 2222 
BUFF_SIZE = 8192
TIMEOUT = 300

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
        try: src.close() 
        except: pass
        try: dst.close() 
        except: pass

def handle_client(client_socket):
    try:
        client_socket.settimeout(TIMEOUT)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        
        request = client_socket.recv(BUFF_SIZE).decode('utf-8', errors='ignore')
        
        # WebSocket अपग्रेड चेक करना (Port 80 और 443 दोनों बग होस्ट के लिए)
        if "upgrade: websocket" in request.lower():
            # स्टेटस लाइन में ही तुम्हारा नाम और रेड कलर का HTML टैग डाल दिया है
            # यह टनल ऐप्स के लॉग्स में सीधा "शिवम बॉस स्विचिंग प्रोटोकॉल" लाल रंग में दिखाएगा
            response = (
                "HTTP/1.1 101 <font color='red'><b>shivam boss</b></font>\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n\r\n"
            )
            client_socket.sendall(response.encode('utf-8'))
            
            # SSH (Dropbear) से कनेक्ट करें
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.settimeout(TIMEOUT)
            target_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            target_socket.connect(('127.0.0.1', TARGET_PORT))
            
            # डेटा ट्रांसफर शुरू करें
            t1 = threading.Thread(target=forward, args=(client_socket, target_socket), daemon=True)
            t2 = threading.Thread(target=forward, args=(target_socket, client_socket), daemon=True)
            t1.start()
            t2.start()
        else:
            # अगर कोई नॉर्मल रिक्वेस्ट है तो बिना क्रैश हुए 200 OK दे दो ताकि कनेक्शन ब्लॉक न हो
            client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nShivam Boss Proxy Running\r\n")
            client_socket.close()
    except Exception as e:
        try: client_socket.close()
        except: pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server.bind(('0.0.0.0', LISTEN_PORT))
    server.listen(500)
    print(f"[*] Proxy listening on port {LISTEN_PORT}...")
    
    while True:
        try:
            client_sock, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
    
