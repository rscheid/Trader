#!/bin/bash

# Container-Name
CONTAINER_NAME="trading_bot_container"


# In den Docker-Container wechseln
echo "Wechsel in die Docker-Shell..."
docker exec -it $CONTAINER_NAME bash
