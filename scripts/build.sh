#!/bin/bash

echo "Building API Showcase Project..."

# Build each service
services=("api-gateway" "user-service" "bff-web" "product-service" "order-service")

for service in "${services[@]}"; do
    echo "Building $service..."
    cd "$service" || exit
    mvn clean package -DskipTests
    cd ..
done

echo "Build completed!"
