# Personal AI Assistant

A local-first, privacy-respecting personal AI assistant with web and CLI interfaces. Built with modern open-source technologies.

## Features

### Phase 1 - MVP (Core Functionality)
- **Chat Interface**: Natural language interaction with local AI
- **Task Management**: Create, update, complete, and delete tasks
- **Notes System**: Save notes with tagging and search
- **Reminders**: Set reminders with recurring options
- **Intent Detection**: AI-powered command parsing
- **Local Storage**: All data stays on your machine by default

### Planned Features
- **Phase 2**: Email drafting, document processing, calendar integration
- **Phase 3**: Multi-step workflows, smart suggestions, automation
- **Phase 4**: Preference learning, custom rules, plugin system

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **LLM**: Ollama with Llama 3 13B
- **Vector Search**: Chroma DB
- **Task Scheduling**: APScheduler

### Frontend
- **Framework**: Next.js (React + TypeScript)
- **Styling**: TailwindCSS
- **State Management**: Zustand

### CLI
- **Framework**: Click/Typer
- **Output Formatting**: Rich

### Deployment
- **Containerization**: Docker & Docker Compose
- **Development**: Local machine with all services

## Quick Start

### Prerequisites
- Docker and Docker Compose
- OR Python 3.11+ and Node.js 18+

### Option 1: Docker (Recommended)

```bash
# Clone and navigate to directory
cd personal-ai-assistant

# Start all services
docker-compose up

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Ollama: http://localhost:11434
```

### Option 2: Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment
cp ../.env.example .env

# Start Ollama separately (download from ollama.com)
ollama serve

# In another terminal:
uvicorn app:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### CLI Setup
```bash
cd backend
python -m cli.main --help
```

## Usage

### Web Interface
Navigate to `http://localhost:3000` to access the web dashboard.

### CLI
```bash
python -m cli.main chat "Create a task to review report by Friday"
python -m cli.main task list
python -m cli.main note create "Important meeting notes" --tags project,urgent
python -m cli.main remind create --task-id <id> --when tomorrow
```

### API
Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
personal-ai-assistant/
├── backend/              # FastAPI application
│   ├── app.py           # Main app entry point
│   ├── config.py        # Configuration
│   ├── core/            # AI engine and intent parsing
│   ├── modules/         # Business logic modules
│   ├── database/        # ORM models and schemas
│   ├── api/             # API routes
│   ├── security/        # Auth and encryption
│   └── tests/           # Test suite
├── frontend/            # Next.js application
├── cli/                 # Command-line interface
├── docker/              # Docker configurations
├── docs/                # Documentation
└── docker-compose.yml   # Local development setup
```

## Configuration

Edit `.env` file to customize:
- LLM model and base URL
- Database connection
- API port and frontend URL
- Logging level
- Encryption keys

See `.env.example` for all available options.

## API Documentation

### Core Endpoints

#### Chat
- `POST /api/v1/chat` - Send message to assistant
- `POST /api/v1/intent` - Analyze intent of message
- `WS /api/v1/chat/ws` - WebSocket for real-time chat

#### Tasks
- `GET /api/v1/tasks` - List tasks
- `POST /api/v1/tasks` - Create task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PUT /api/v1/tasks/{id}/complete` - Mark as complete

#### Notes
- `GET /api/v1/notes` - List notes
- `POST /api/v1/notes` - Create note
- `GET /api/v1/notes/{id}` - Get note
- `PUT /api/v1/notes/{id}` - Update note
- `DELETE /api/v1/notes/{id}` - Delete note
- `GET /api/v1/notes/_search` - Search notes

#### Reminders
- `GET /api/v1/reminders` - List reminders
- `POST /api/v1/reminders` - Create reminder
- `GET /api/v1/reminders/_upcoming` - Get upcoming
- `POST /api/v1/reminders/{id}/_trigger` - Trigger reminder

Interactive API docs available at `/docs` endpoint.

## Security

- **Local First**: Data stays local by default
- **Encryption**: Sensitive data encrypted at rest
- **No External Calls**: PII never sent to external systems
- **Audit Logging**: All operations logged
- **Permission System**: Built-in access control

## Development

### Running Tests
```bash
cd backend
pytest tests/ -v
```

### Code Style
```bash
black .
flake8 .
mypy .
```

### Database Migrations
```bash
cd backend
alembic init migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Roadmap

- [x] Phase 1: MVP with core modules
- [ ] Phase 2: Email and document integration
- [ ] Phase 3: Workflow automation
- [ ] Phase 4: Personalization and learning
- [ ] Mobile app support
- [ ] Advanced NLU capabilities
- [ ] Multi-user support (self-hosted)

## Contributing

This is a personal project, but contributions are welcome via pull requests.

## License

MIT License - See LICENSE file

## Support

For issues, questions, or suggestions, please open an issue on the repository.

## Disclaimer

This is a local-first AI assistant. It respects user privacy and keeps data local by default. When using external LLM services (optional), review their privacy policies.
