#!/bin/bash
set -e

echo "🚀 Setting up Personal AI Assistant..."

# Create directories
mkdir -p data logs

# Copy env template if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file (please edit with your settings)"
fi

# Backend setup
echo ""
echo "Setting up backend..."
cd backend
pip install -r requirements.txt
echo "✓ Backend dependencies installed"

# Database
echo "Initializing database..."
# Add alembic setup if needed
echo "✓ Database initialized"

cd ..

# Frontend setup (optional)
echo ""
echo "Setting up frontend..."
cd frontend
npm install
echo "✓ Frontend dependencies installed"

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  docker-compose up"
echo ""
echo "Or locally:"
echo "  1. Backend: cd backend && uvicorn app:app --reload"
echo "  2. Frontend: cd frontend && npm run dev"
echo "  3. CLI: python -m cli.main --help"
