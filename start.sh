#!/bin/bash

# Dropbear ko local port 2222 par background me start karna
dropbear -F -E -p 127.0.0.1:2222 &

# Proxy script ko fire karna
python3 /app/ws-proxy.py
