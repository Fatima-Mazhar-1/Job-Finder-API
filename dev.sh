#!/bin/bash

# Function to stop all processes on exit
cleanup() {
    echo "Stopping all processes..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up the trap to catch SIGINT (Ctrl+C)
trap cleanup SIGINT

# Start the backend
echo "Starting the backend server..."
python run.py &

# Wait for the backend to start
sleep 3

# Start the frontend
echo "Starting the frontend server..."
cd frontend && npm start &

# Keep the script running
wait 