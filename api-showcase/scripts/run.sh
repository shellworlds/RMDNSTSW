#!/bin/bash

echo "Starting API Showcase Project..."

# Start all services with Docker Compose
docker-compose down
docker-compose up -d

echo ""
echo "Services starting... Please wait 30 seconds."
echo ""
echo "Available Services:"
echo "  API Gateway: http://localhost:8080"
echo "  Eureka:      http://localhost:8761"
echo "  User Service: http://localhost:8081"
echo "  BFF Web:     http://localhost:8084"
echo ""
echo "Test with: curl http://localhost:8080/actuator/health"
