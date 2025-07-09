#!/bin/bash

echo "========================================"
echo "   Failure Analysis Flask App"
echo "========================================"
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Starting Flask application..."
echo "The web application will be available at: http://localhost:8080"
echo "Press Ctrl+C to stop the server"
echo ""
python3 app.py 