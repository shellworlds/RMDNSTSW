#!/bin/bash

echo "Testing API Endpoints..."
echo "========================"

# Wait for services to start
sleep 5

# Test API Gateway
echo "1. Testing API Gateway Health:"
curl -s http://localhost:8080/actuator/health | jq .status || echo "Not ready"

# Test User Service via API Gateway
echo ""
echo "2. Testing User Service:"
curl -s "http://localhost:8080/api/v1/users?page=0&size=2" | jq . || echo "Failed"

# Test BFF Web
echo ""
echo "3. Testing BFF Web:"
curl -s http://localhost:8080/web/api/dashboard/summary | jq . || echo "Failed"

echo ""
echo "API Testing Complete!"
