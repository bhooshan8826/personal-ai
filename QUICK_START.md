# Personal AI Assistant - Quick Start Guide

## ✅ Project Status

**GitHub Repository**: https://github.com/bhooshan8826/personal-ai
**Status**: ✅ Pushed and Ready
**Branch**: master

---

## 🚀 How to Run

### Option 1: Docker (Recommended - Easiest)

#### Prerequisites
- Docker Desktop installed (https://www.docker.com/products/docker-desktop)

#### Steps
```bash
cd "d:\Personal AI"
docker-compose up
```

Wait for all services to start. Then visit:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Backend**: http://localhost:8000

**Ctrl+C** to stop all services.

---

### Option 2: Local Development (Advanced)

#### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama (download from https://ollama.com)

#### Terminal 1: Start Ollama (LLM Service)
```bash
# Download Ollama from https://ollama.com
# Run Ollama
ollama serve

# In another terminal, pull Llama 3:
ollama pull llama3
```

#### Terminal 2: Start Backend
```bash
cd "d:\Personal AI\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Backend will be available at: http://localhost:8000

#### Terminal 3: Start Frontend
```bash
cd "d:\Personal AI\frontend"
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

#### Terminal 4: Use CLI (Optional)
```bash
cd "d:\Personal AI"
python -m cli.main chat "Create a task to review the report"
python -m cli.main task list
python -m cli.main note create "Meeting notes" --tags important
```

---

## 💡 Usage Examples

### Web Interface
1. Open http://localhost:3000
2. Click "Start Chatting" or go to Chat tab
3. Type natural language commands like:
   - "Create a task to send email by Friday"
   - "Save a note about project ideas"
   - "Remind me to review the report tomorrow"

### API (Programmatic)
- API Docs: http://localhost:8000/docs
- Base URL: http://localhost:8000
- Example:
  ```bash
  curl -X POST http://localhost:8000/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Create a task to review the report"}'
  ```

### CLI
```bash
pai chat "Your message here"
pai task create "Task title"
pai task list
pai task complete <task-id>
pai note create "Note content"
pai note list
pai reminder list
pai health
```

---

## 🔧 Configuration

Edit `.env` file to customize:
```
APP_ENV=development
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
DATABASE_URL=sqlite:///./data/app.db
API_PORT=8000
DEBUG=true
```

---

## 📁 Project Structure
```
personal-ai/
├── backend/          # FastAPI server
├── frontend/         # React/Next.js UI
├── cli/              # Command-line tool
├── docker/           # Docker configuration
├── docker-compose.yml
├── README.md
└── IMPLEMENTATION_SUMMARY.md
```

---

## 🚨 Troubleshooting

### "Connection refused" / "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check it's accessible: http://localhost:11434
- Wait 5-10 seconds for Ollama to pull the model

### "Port 8000 already in use"
- Stop other services using port 8000
- Or change `API_PORT` in `.env`

### "Port 3000 already in use"
- Stop other services using port 3000
- Or run frontend on different port: `npm run dev -- -p 3001`

### Python package installation fails
- Try: `pip install --upgrade pip`
- Then: `pip install -r requirements.txt --no-cache-dir`

### Frontend doesn't load
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console (F12) for errors
- Verify backend is running (check http://localhost:8000/docs)

---

## 📊 What You Can Do

### Create Tasks ✓
- "Remind me to send the report by Friday"
- "Create a high-priority task: Review code changes"
- "Add task: Follow up with team tomorrow morning"

### Create Notes ✓
- "Save this: Project meeting notes..."
- "Remember: Key discussion points were..."
- Create and search notes by tag

### Set Reminders ✓
- "Remind me to check email in 30 minutes"
- "Schedule a reminder for tomorrow at 9am"
- Recurring reminders (daily, weekly)

### Chat with AI ✓
- Natural language understanding
- Intent detection and action execution
- Context-aware responses

---

## 🧪 Testing the System

### Quick Test
```bash
# 1. Verify API is running
curl http://localhost:8000/api/v1/health

# 2. Create a task via API
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "priority": "high"}'

# 3. List tasks
curl http://localhost:8000/api/v1/tasks

# 4. Chat with AI
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

---

## 📝 API Documentation

Visit http://localhost:8000/docs for interactive API documentation

Key endpoints:
- `POST /api/v1/chat` - Chat with AI
- `GET/POST /api/v1/tasks` - Manage tasks
- `GET/POST /api/v1/notes` - Manage notes
- `GET/POST /api/v1/reminders` - Set reminders
- `GET /api/v1/health` - Check API status

---

## 🔐 Security Notes

- All data stays local by default
- No external API calls for personal data
- Database file is in `data/` directory
- Sensitive data can be encrypted (feature ready)
- Settings in `.env` are not committed to Git

---

## 📦 System Requirements

### Docker Way (Easiest)
- Docker Desktop
- 4GB RAM recommended
- 2GB disk space

### Local Way
- Python 3.11+
- Node.js 18+
- Ollama
- 4GB RAM
- 3GB disk space

---

## 🎯 Next Steps

1. **Try it out** - Run using Docker or locally
2. **Create some tasks/notes** - Via web or CLI
3. **Explore the API** - Visit /docs endpoint
4. **Customize** - Edit `.env` for your needs
5. **Extend** - Add new features in Phase 2

---

## 📚 Documentation

- `README.md` - Project overview
- `IMPLEMENTATION_SUMMARY.md` - Detailed technical breakdown
- In-code docstrings and comments
- API docs at http://localhost:8000/docs

---

## 💬 Features Summary

✅ **Chat Interface** - Talk to local AI
✅ **Task Management** - Create, complete tasks
✅ **Notes System** - Save and search notes
✅ **Reminders** - Schedule reminders
✅ **Intent Detection** - Understand natural language
✅ **Local Storage** - All data stays on your machine
✅ **Web Dashboard** - Beautiful React UI
✅ **CLI Tool** - Command-line interface
✅ **RESTful API** - Programmatic access
✅ **Docker Ready** - Easy deployment

---

## 🚀 You're ready to go!

**GitHub Repo**: https://github.com/bhooshan8826/personal-ai

Choose your preferred method above and start using your personal AI assistant! 🎉
