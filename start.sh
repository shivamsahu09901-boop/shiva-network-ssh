#!/bin/bash

# Dropbear ko optimized settings ke saath start karo
dropbear -F -E -p 127.0.0.1:2222 -K 60 -I 300 &

# Wait for dropbear to start
sleep 2

# Proxy script start karo
python3 /app/ws-proxy.py
