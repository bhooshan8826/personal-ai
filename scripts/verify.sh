#!/bin/bash
# Verification script for Personal AI Assistant

echo "🔍 Personal AI Assistant - System Verification"
echo "=============================================="
echo ""

# Check Python
echo "✓ Checking Python..."
python --version
echo ""

# Check Node.js
echo "✓ Checking Node.js..."
which node > /dev/null 2>&1 && node --version || echo "⚠️  Node.js not found (needed for frontend)"
echo ""

# Check Docker
echo "✓ Checking Docker..."
which docker > /dev/null 2>&1 && docker --version || echo "⚠️  Docker not found (optional but recommended)"
echo ""

# Check project files
echo "✓ Checking project structure..."
files_count=$(find . -type f \( -name "*.py" -o -name "*.tsx" -o -name "*.ts" \) -not -path "./.git/*" | wc -l)
echo "  Found $files_count source files"
echo ""

# List key files
echo "✓ Key configuration files:"
ls -1 .env.example docker-compose.yml README.md 2>/dev/null | sed 's/^/  ✓ /'
echo ""

# Check directories
echo "✓ Project directories:"
for dir in backend frontend cli docker docs scripts; do
  if [ -d "$dir" ]; then
    echo "  ✓ $dir/"
  else
    echo "  ✗ $dir/ (missing)"
  fi
done
echo ""

# Git status
echo "✓ Git status:"
git log --oneline -2 | sed 's/^/  /'
echo ""

# Remote
echo "✓ Git remote:"
git remote -v | sed 's/^/  /'
echo ""

echo "✅ Verification complete!"
echo ""
echo "📖 To get started, see QUICK_START.md"
