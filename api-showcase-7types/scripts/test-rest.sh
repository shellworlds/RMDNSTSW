#!/bin/bash
echo "Testing REST API..."
echo "==================="

echo "1. GET /api/v1/users"
curl -s "http://localhost:8080/rest/api/v1/users?page=0&size=2" | jq .

echo ""
echo "2. GET /api/v1/users/1"
curl -s "http://localhost:8080/rest/api/v1/users/1" | jq .

echo ""
echo "3. POST /api/v1/users"
curl -s -X POST "http://localhost:8080/rest/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","email":"test@example.com","firstName":"Test","lastName":"User"}' | jq .

echo ""
echo "✅ REST API Test Complete"
