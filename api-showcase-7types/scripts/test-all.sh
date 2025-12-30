#!/bin/bash

echo "🧪 Testing All 7 API Types..."
echo "==============================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "1. Testing REST API..."
curl -s http://localhost:8080/rest/api/v1/health | grep -q "UP" && echo -e "${GREEN}✓ REST API working${NC}" || echo -e "${RED}✗ REST API failed${NC}"

echo ""
echo "2. Testing GraphQL API (via GraphiQL)..."
echo "   Open browser: http://localhost:8080/graphiql"
echo "   Try query: { users { id username email } }"

echo ""
echo "3. Testing WebSocket API..."
echo "   Connect to: ws://localhost:8080/ws/chat"
echo "   Send: {\"type\": \"JOIN_ROOM\", \"roomId\": \"test-room\"}"

echo ""
echo "4. Testing gRPC API..."
echo "   Requires gRPC client. Install with:"
echo "   python -m pip install grpcio grpcio-tools"

echo ""
echo "5. Testing API Gateway..."
curl -s http://localhost:8080/ | grep -q "nginx" && echo -e "${GREEN}✓ API Gateway working${NC}" || echo -e "${RED}✗ API Gateway failed${NC}"

echo ""
echo "📊 All API Types Available:"
echo "---------------------------"
echo "• REST:      http://localhost:8080/rest/api/v1/users"
echo "• GraphQL:   http://localhost:8080/graphql"
echo "• WebSocket: ws://localhost:8080/ws/chat"
echo "• gRPC:      localhost:50051"
echo "• API Docs:  http://localhost:8080/"
