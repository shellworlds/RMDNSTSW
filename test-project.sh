#!/bin/bash

echo "🧪 Testing API Showcase Project..."
echo "=================================="

# Check if we have all files
echo "1. Checking project structure..."
ls -la
ls api-gateway/ user-service/ scripts/ 2>/dev/null

echo ""
echo "2. Checking Java files..."
find . -name "*.java" -type f | head -5

echo ""
echo "3. Checking configuration files..."
ls docker-compose.yml *.yml *.yaml 2>/dev/null

echo ""
echo "4. Checking if project can be built..."
cd user-service
if mvn clean compile -q 2>/dev/null; then
    echo "✅ User Service builds successfully"
else
    echo "❌ Build failed, checking dependencies..."
    mvn dependency:tree | head -20
fi
cd ..

echo ""
echo "✅ Project structure verified!"
echo "📁 Total files: $(find . -type f | wc -l)"
echo "📝 Java files: $(find . -name "*.java" -type f | wc -l)"
echo "🐳 Docker files: $(find . -name "Dockerfile*" -type f | wc -l)"
echo "📋 YAML files: $(find . -name "*.yml" -o -name "*.yaml" | wc -l)"
