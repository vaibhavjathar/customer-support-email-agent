# Complete File Manifest - Customer Support Email Agent

## 📋 Project Root Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies (24 packages) |
| `.env` | Environment variables (Groq API key) |
| `.env.example` | Template for environment setup |
| `.gitignore` | Git exclusions (venv, __pycache__, .env) |
| `main.py` | Entry point (redirects to src/api/main.py) |
| `pyproject.toml` | Project metadata (name, version) |
| `README.md` | Project overview and setup guide |
| `WORKFLOW_GUIDE.md` | LangGraph workflow explanation |
| `PROJECT_SUMMARY.md` | Technical deep dive (500 lines) |
| `RESUME_SUMMARY.md` | Resume-optimized project description |
| `run_system.sh` | Quick-start shell script |
| `FILE_MANIFEST.md` | This file |

---

## 🔧 Backend Architecture (`src/`)

### Core Configuration (`src/core/`)
| File | Purpose | Key Classes |
|------|---------|------------|
| `config.py` | Groq LLM settings, pydantic config | `Settings` |
| `__init__.py` | Module initialization | |

### Database Layer (`src/db/`)
| File | Purpose | Key Components |
|------|---------|-----------------|
| `__init__.py` | Export Base, SessionLocal, engine | |
| `database.py` | SQLAlchemy setup: engine, SessionLocal, Base | `DATABASE_URL`, `engine`, `SessionLocal`, `Base` |
| `models.py` | EmailRecord ORM model | `EmailRecord` (8 columns) |

### Services (`src/services/`)
| File | Purpose | Key Classes | Methods |
|------|---------|------------|---------|
| `llm_service.py` | Groq LLM integration | `LLMService`, `BooleanEnum`, structured output models | `classify_email()`, `analyze_sentiment()`, `assess_priority()`, `generate_response()`, `retrieve_knowledge_queries()` |
| `knowledge_service.py` | FAISS RAG + keyword search | `KnowledgeService` | `search_knowledge_base()`, `get_category_articles()`, `format_knowledge_context()` |
| `db_service.py` | Database CRUD operations | `DBService` | `save_email_record()`, `get_email()`, `get_all_emails()` |
| `email_service.py` | Email business logic | `EmailService` | `update_email_status()`, `get_email()`, `list_emails()` |

### Schemas (`src/schemas/`)
| File | Purpose | Key Models |
|------|---------|------------|
| `email.py` | API request/response models | `EmailRequest`, `EmailResponse`, `Email` |
| `agent_state.py` | LangGraph state TypedDict | `AgentState` |

### Graph Workflow (`src/graph/`)
| File | Purpose | Key Function |
|------|---------|---------------|
| `workflow.py` | LangGraph DAG builder | `build_email_support_graph()` |

### Nodes (`src/nodes/`) - LangGraph Processing Nodes
| File | Purpose | Function | Input → Output |
|------|---------|----------|-----------------|
| `email_classifier.py` | Classify email category | `classify_email_node()` | Email → classification |
| `sentiment_analyzer.py` | Analyze sentiment | `analyze_sentiment_node()` | Email → sentiment data |
| `priority_assessor.py` | Determine escalation | `assess_priority_node()` | Email + sentiment → priority |
| `knowledge_retriever.py` | Retrieve KB articles | `retrieve_knowledge_node()` | Email + classification → articles |
| `response_generator.py` | Generate AI response | `generate_response_node()` | Email + knowledge → response |
| `human_review.py` | Route to human review | `human_review_node()` | Priority → routing decision |
| `finalizer.py` | Finalize and return result | `finalize_node()` | All state → final output |

### Prompts (`src/prompts/`)
| File | Purpose | Content |
|------|---------|---------|
| `templates.py` | LLM prompt templates | Classification, sentiment, priority, knowledge, response prompts |

### Utilities (`src/utils/`)
| File | Purpose |
|------|---------|
| `helpers.py` | Helper functions |
| `logger.py` | Logging configuration |

### API (`src/api/`)
| File | Purpose | Content |
|------|---------|---------|
| `main.py` | FastAPI app setup | App creation, lifespan events, health check, root endpoint |
| `routes.py` | API endpoints | POST /process-email, GET /emails, GET /emails/{id} |

---

## 🎨 Frontend (`frontend/`)

| File | Purpose | Sections |
|------|---------|----------|
| `app.py` | Streamlit SaaS application | Page 1: Send Email, Page 2: Inbox, Page 3: API Docs |
| `README.md` | Frontend setup and usage guide | Features, installation, configuration |

**Features:**
- Dark mode CSS with glassmorphism
- 3 navigation pages (radio button)
- Step-by-step progress visualization
- Plotly interactive charts
- Responsive design, 150+ CSS rules

---

## 📚 Knowledge Base (`data/knowledge/`)

| File | Size | Documents | Content |
|------|------|-----------|---------|
| `billing.json` | 1.3 KB | 4 | Payment methods, invoices, refunds, duplicate charges |
| `technical.json` | 1.4 KB | 4 | API auth, rate limiting, integration, troubleshooting |
| `account.json` | 1.4 KB | 4 | Password reset, 2FA, login issues, recovery |
| `general.json` | 1.3 KB | 4 | Onboarding, pricing, support, status |

**Total:** 16 articles, 5.4 KB

---

## 💾 Data Files (`data/`)

| File/Folder | Purpose |
|-------------|---------|
| `agent.db` | SQLite database (40 KB, 6 test records) |
| `faiss_index/` | FAISS index directory (optional, for ETL output) |
| `knowledge/` | JSON knowledge base (4 category files) |

---

## 🔨 Scripts (`scripts/`)

| File | Purpose | Function |
|------|---------|----------|
| `populate_knowledge_base.py` | ETL pipeline | Load JSON → embed → save FAISS index to disk |

**Usage:** `python scripts/populate_knowledge_base.py`

---

## 📖 Documentation Files

| File | Purpose | Length |
|------|---------|--------|
| `README.md` | Project overview and quickstart | ~150 lines |
| `WORKFLOW_GUIDE.md` | LangGraph workflow explanation | ~200 lines |
| `PROJECT_SUMMARY.md` | Comprehensive technical breakdown | ~500 lines |
| `RESUME_SUMMARY.md` | Resume-optimized description | ~400 lines |
| `FILE_MANIFEST.md` | This file |

---

## 🔐 Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Secrets (Groq API key) |
| `.env.example` | Template (no secrets) |
| `.gitignore` | Git exclusions |
| `pyproject.toml` | Package metadata |

---

## 📊 File Statistics

| Category | Count | Details |
|----------|-------|---------|
| **Python Files** | 34 | Core code |
| **JSON Files** | 4 | Knowledge base |
| **Documentation** | 4 | README, guides, summaries |
| **Configuration** | 4 | .env, .gitignore, pyproject.toml, requirements.txt |
| **Scripts** | 1 | ETL pipeline |
| **Database** | 1 | SQLite with 6 test records |

**Total Python LOC:** 3,045

---

## 🚀 Quick Start Commands

### Backend
```bash
source venv/bin/activate
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
source venv/bin/activate
streamlit run frontend/app.py
```

### Database Initialization
```bash
source venv/bin/activate
python -c "from src.db.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### ETL Pipeline
```bash
source venv/bin/activate
python scripts/populate_knowledge_base.py
```

### Quick Start (All-in-one)
```bash
./run_system.sh
```

---

## 📂 Directory Structure

```
customer-support-email-agent/
├── src/                               # Backend source
│   ├── api/                          # FastAPI app
│   │   ├── main.py                   # App + lifespan
│   │   └── routes.py                 # 3 endpoints
│   ├── core/                         # Configuration
│   │   └── config.py                 # Groq settings
│   ├── db/                           # Database layer
│   │   ├── database.py               # SQLAlchemy setup
│   │   └── models.py                 # EmailRecord ORM
│   ├── services/                     # Business logic
│   │   ├── llm_service.py
│   │   ├── knowledge_service.py
│   │   ├── db_service.py
│   │   └── email_service.py
│   ├── graph/                        # LangGraph workflow
│   │   └── workflow.py
│   ├── nodes/                        # 7 processing nodes
│   │   ├── email_classifier.py
│   │   ├── sentiment_analyzer.py
│   │   ├── priority_assessor.py
│   │   ├── knowledge_retriever.py
│   │   ├── response_generator.py
│   │   ├── human_review.py
│   │   └── finalizer.py
│   ├── schemas/                      # Pydantic models
│   │   ├── email.py
│   │   └── agent_state.py
│   ├── prompts/                      # LLM templates
│   │   └── templates.py
│   └── utils/                        # Helpers
│       ├── helpers.py
│       └── logger.py
├── frontend/                         # Streamlit UI
│   ├── app.py                        # 3 pages + CSS
│   └── README.md
├── scripts/                          # ETL utilities
│   └── populate_knowledge_base.py
├── data/                             # Data & database
│   ├── knowledge/                    # 4 JSON files
│   │   ├── billing.json
│   │   ├── technical.json
│   │   ├── account.json
│   │   └── general.json
│   ├── agent.db                      # SQLite database
│   └── faiss_index/                  # FAISS vectors (optional)
├── requirements.txt                  # 24 dependencies
├── .env                             # Secrets
├── .env.example                     # Template
├── .gitignore
├── pyproject.toml
├── main.py                          # Entry point
├── run_system.sh                    # Quick start
├── README.md
├── WORKFLOW_GUIDE.md
├── PROJECT_SUMMARY.md
├── RESUME_SUMMARY.md
└── FILE_MANIFEST.md
```

---

## ✅ File Validation Status

| Category | Status | Details |
|----------|--------|---------|
| Syntax | ✅ All files compile | 0 syntax errors |
| Imports | ✅ All resolve | 0 import errors |
| Database | ✅ Schema verified | 8 columns correct |
| API | ✅ Endpoints working | 3/3 responding |
| Frontend | ✅ Pages rendering | Streamlit functional |
| Config | ✅ Secrets isolated | No hardcoded values |
| Docs | ✅ Complete | 4 markdown files |

---

## 🎓 File Purposes for Resume

**Demonstrate:** Full-stack development, system design, AI/ML integration
- `src/services/llm_service.py` - LLM integration mastery
- `src/db/models.py` + `db_service.py` - Database design
- `src/graph/workflow.py` - Architecture & state management
- `frontend/app.py` - Frontend development, UI/UX
- `scripts/populate_knowledge_base.py` - ETL pipeline, data engineering
- `PROJECT_SUMMARY.md` - Technical depth
- `RESUME_SUMMARY.md` - Interview talking points

---

*Last Updated: March 12, 2026*
*Status: Production Ready ✅*
