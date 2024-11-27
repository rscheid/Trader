#!/bin/bash

# Pull the latest changes from GitHub
echo "Pulling latest changes from GitHub..."
git pull origin main

# Build the Docker image
echo "Building Docker image..."
docker build -t trading-bot-rsi .

# Stop and remove the old container
echo "Stopping and removing old container..."
docker stop trading_bot_container || true
docker rm trading_bot_container || true

# Start the new container
echo "Starting new container..."
docker run -d --name trading_bot_container -p 3000:3000 trading-bot-rsi

echo "Deployment complete."
