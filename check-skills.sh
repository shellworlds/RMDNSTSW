#!/bin/bash

echo "🔍 Analyzing Your API Showcase Skills..."
echo "========================================"

cd ~/RMDNSTSW/api-showcase

echo ""
echo "📁 Project Structure:"
tree -I 'target|.git|*.class' --dirsfirst -L 3

echo ""
echo "💻 Languages Detected:"
echo "---------------------"

# Count by file type
echo "Java (Spring Boot):"
find . -name "*.java" -type f | wc -l
echo "  Examples:"
find . -name "*.java" -type f | head -3 | sed 's/^/    - /'

echo ""
echo "Docker (Containerization):"
find . -name "Dockerfile*" -type f | wc -l
echo "  Files:"
find . -name "Dockerfile*" -type f | sed 's/^/    - /'

echo ""
echo "YAML (Configuration):"
find . \( -name "*.yml" -o -name "*.yaml" \) -type f | wc -l
echo "  Files:"
find . \( -name "*.yml" -o -name "*.yaml" \) -type f | sed 's/^/    - /'

echo ""
echo "SQL (Database):"
find . -name "*.sql" -type f | wc -l

echo ""
echo "Shell (DevOps):"
find . -name "*.sh" -type f | wc -l
echo "  Scripts:"
find . -name "*.sh" -type f | sed 's/^/    - /'

echo ""
echo "📊 Summary:"
echo "----------"
TOTAL_FILES=$(find . -type f | wc -l)
JAVA_FILES=$(find . -name "*.java" -type f | wc -l)
DOCKER_FILES=$(find . -name "Dockerfile*" -type f | wc -l)
YAML_FILES=$(find . \( -name "*.yml" -o -name "*.yaml" \) -type f | wc -l)

echo "Total files in API showcase: $TOTAL_FILES"
echo "Java files (backend logic): $JAVA_FILES ($((JAVA_FILES * 100 / TOTAL_FILES))%)"
echo "Docker files (containerization): $DOCKER_FILES"
echo "YAML files (configuration): $YAML_FILES"

echo ""
echo "🎯 Skills Demonstrated:"
echo "----------------------"
echo "1. Java 17 + Spring Boot 3.1"
echo "2. Microservices Architecture"
echo "3. Docker Containerization"
echo "4. PostgreSQL Database Design"
echo "5. Redis Caching Strategies"
echo "6. API Gateway Pattern"
echo "7. Rate Limiting Implementation"
echo "8. Circuit Breaker Pattern"
echo "9. BFF (Backend for Frontend)"
echo "10. CI/CD with GitHub Actions"
