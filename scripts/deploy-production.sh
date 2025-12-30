#!/bin/bash
# Production deployment script for API Showcase

set -e  # Exit on error

echo "🚀 Deploying API Showcase to Production..."

# Build Docker images
echo "Building Docker images..."
docker-compose build

# Run tests
echo "Running tests..."
docker-compose run --rm user-service mvn test || {
    echo "Tests failed! Aborting deployment."
    exit 1
}

# Deploy to production
echo "Starting production services..."
docker-compose up -d

# Health check
echo "Performing health checks..."
sleep 30
curl -f http://localhost:8080/api/v1/health || {
    echo "Health check failed!"
    exit 1
}

echo "✅ Deployment successful!"
echo "📡 Services running:"
echo "   - API Gateway: http://localhost:8080"
echo "   - User Service: http://localhost:8081"
echo "   - PostgreSQL: localhost:5432"
