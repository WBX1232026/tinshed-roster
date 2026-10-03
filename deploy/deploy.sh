#!/bin/bash
set -e

echo "Building Docker image..."
docker build -t tinshed-roster .

echo "Running container..."
docker run -d -p 5000:5000 --name tinshed-roster tinshed-roster

echo "Deployed at http://localhost:5000"
