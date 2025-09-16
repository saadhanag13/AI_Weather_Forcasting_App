#!/bin/bash

# Project Structure Checker for AI Weather Forecast App
echo "🔍 Checking AI Weather Forecast Project Structure..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check function
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1"
        return 0
    else
        echo -e "${RED}❌${NC} $1 (missing)"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅${NC} $1/"
        return 0
    else
        echo -e "${RED}❌${NC} $1/ (missing)"
        return 1
    fi
}

# Initialize counters
missing_count=0

echo ""
echo "📁 Directory Structure:"
check_dir "backend" || ((missing_count++))
check_dir "frontend" || ((missing_count++))
check_dir "scripts" || ((missing_count++))
check_dir "logs" || ((missing_count++))

echo ""
echo "🐳 Docker Files:"
check_file "docker-compose.yml" || ((missing_count++))
check_file "backend/Dockerfile" || ((missing_count++))
check_file "frontend/Dockerfile" || ((missing_count++))
check_file ".dockerignore" || ((missing_count++))

echo ""
echo "📋 Requirements:"
check_file "backend/requirements.txt" || ((missing_count++))
check_file "frontend/requirements.txt" || ((missing_count++))

echo ""
echo "📱 Application Files:"
check_file "backend/main.py" || ((missing_count++))
check_file "frontend/app.py" || ((missing_count++))

echo ""
echo "🤖 Your Model Files:"
check_file "backend/model_loader.py" || ((missing_count++))
check_file "backend/data_fetcher.py" || ((missing_count++))
check_file "backend/model_utils.py" || ((missing_count++))
check_file "backend/global_weather_saved_model.keras" || ((missing_count++))

echo ""
echo "⚙️  Configuration Files:"
check_file "backend/.env" || echo -e "${YELLOW}⚠️${NC}  backend/.env (will be created by setup.sh)"
check_file "frontend/.env" || echo -e "${YELLOW}⚠️${NC}  frontend/.env (will be created by setup.sh)"

echo ""
echo "🔧 Scripts:"
check_file "scripts/setup.sh" || ((missing_count++))
check_file "scripts/build.sh" || ((missing_count++))
check_file "scripts/deploy.sh" || ((missing_count++))

# Check if scripts are executable
echo ""
echo "🔐 Script Permissions:"
for script in scripts/*.sh; do
    if [ -x "$script" ]; then
        echo -e "${GREEN}✅${NC} $script (executable)"
    else
        echo -e "${YELLOW}⚠️${NC}  $script (not executable - run: chmod +x $script)"
    fi
done

# Summary
echo ""
echo "📊 Summary:"
if [ $missing_count -eq 0 ]; then
    echo -e "${GREEN}🎉 All essential files are present!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./scripts/setup.sh"
    echo "2. Run: ./scripts/build.sh"
else
    echo -e "${RED}❌ $missing_count files/directories are missing${NC}"
    echo ""
    echo "What to do:"
    echo "1. Create missing directories"
    echo "2. Move your files to the correct locations"
    echo "3. Run: ./scripts/setup.sh"
    echo "4. Run this checker again"
fi

echo ""
echo "📝 File Movement Guide:"
echo "   Your current main.py → backend/main.py"
echo "   Your current app.py → frontend/app.py" 
echo "   Your model file → backend/models/weather_model.keras"
echo "   Your supporting modules → backend/ directory"