# Customer Support Email Agent

A **LangGraph-based Customer Support Email Agent** built with FastAPI, LangChain, and OpenAI. This agent intelligently processes incoming customer support emails, analyzes sentiment, retrieves relevant knowledge base articles, and generates context-aware, professional responses.

## 🎯 Features

- **Email Classification** - Automatically categorize emails (billing, technical, account, complaint, refund, etc.)
- **Sentiment Analysis** - Detect customer sentiment and frustration levels
- **Knowledge Base Integration** - Retrieve relevant FAQ and support articles
- **Intelligent Response Generation** - Generate professional, empathetic responses using GPT-4
- **Priority Assessment** - Determine urgency and escalation needs
- **Extensible Workflow** - LangGraph-based workflow for easy customization

## 🛠 Tech Stack

- **Python 3.12** - Latest Python version
- **FastAPI** - Modern, fast API framework
- **LangGraph** - Graph-based AI workflow orchestration
- **LangChain** - LLM framework and utilities
- **LangChain OpenAI** - OpenAI integration
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server

## 📁 Project Structure

```
customer-support-email-agent/
├── data/                    # Knowledge base and customer data
├── src/
│   ├── api/                 # FastAPI endpoints and routes
│   ├── core/                # Configuration and settings
│   ├── graph/               # LangGraph workflow definitions
│   ├── nodes/               # Individual workflow nodes
│   ├── services/            # Business logic and integrations
│   ├── prompts/             # LLM prompt templates
│   ├── schemas/             # Pydantic models
│   └── utils/               # Utility functions
├── test/                    # Test suite
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (template)
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+**
- **OpenAI API Key** (from https://platform.openai.com)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd customer-support-email-agent
```

2. **Create a virtual environment:**
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
# Edit .env and add your OpenAI API key
nano .env  # or open with your preferred editor
```

Update the following required variables:
```
OPENAI_API_KEY=sk-your-key-here
```

5. **Run the application:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/v1/process-email" \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "customer@example.com",
    "to_email": "support@company.com",
    "subject": "Billing question about my subscription",
    "body": "Hi, I was charged twice this month. Can you help?",
    "customer_name": "John Doe",
    "customer_id": "cust_123"
  }'
```

## 🔄 Workflow Overview

The agent follows this LangGraph workflow:

1. **Classify Email** - Categorize the email type
2. **Analyze Sentiment** - Detect emotion and urgency
3. **Retrieve Knowledge** - Search knowledge base for relevant articles
4. **Generate Response** - Create an intelligent response
5. **Assess Priority** - Determine if escalation is needed
6. **Finalize** - Prepare output and suggested actions

## 💾 Configuration

All configuration is managed through environment variables in `.env`:

```ini
# OpenAI Settings
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000

# Application Settings
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=INFO

# Server Settings
HOST=0.0.0.0
PORT=8000
```

## 🧪 Testing

Run the test suite:
```bash
pytest test/
```

Run tests with coverage:
```bash
pytest test/ --cov=src --cov-report=html
```

## 📝 Modules Overview

### `src/api/` - API Layer
- **main.py** - FastAPI application setup
- **routes.py** - API endpoints for email processing

### `src/graph/` - Workflow Orchestration
- **workflow.py** - LangGraph definition with all nodes

### `src/nodes/` - Processing Nodes
- **email_classifier.py** - Email categorization
- **sentiment_analyzer.py** - Sentiment detection
- **knowledge_retriever.py** - Knowledge base search
- **response_generator.py** - Response generation
- **priority_assessor.py** - Priority assessment
- **finalizer.py** - Output preparation

### `src/services/` - Business Logic
- **llm_service.py** - OpenAI interactions
- **email_service.py** - Email management
- **knowledge_service.py** - Knowledge base management

### `src/prompts/` - LLM Prompts
- **templates.py** - Prompt templates for various tasks

### `src/schemas/` - Data Models
- **email.py** - Email request/response schemas
- **agent_state.py** - Workflow state definition

## 🔐 Security

- Never commit `.env` files with real API keys
- Use environment variables for all sensitive data
- API key should be kept private and never shared
- All input is validated with Pydantic

## 📦 Dependencies

See `requirements.txt` for full list. Key dependencies:
- `langchain==0.1.9`
- `langgraph==0.0.26`
- `langchain-openai==0.0.8`
- `fastapi==0.104.1`
- `pydantic==2.5.0`

## 🚧 Development

### Format Code
```bash
black src/ test/
isort src/ test/
```

### Lint Code
```bash
ruff check src/ test/
```

## 📋 Features Roadmap

- [ ] Multi-turn conversation support
- [ ] Email sending integration (SMTP)
- [ ] Database persistence (PostgreSQL)
- [ ] Email attachment handling
- [ ] Advanced NLP analysis
- [ ] Custom knowledge base loading
- [ ] Response templates
- [ ] Analytics dashboard
- [ ] Rate limiting
- [ ] User authentication

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the API docs at `/docs`

## 🙏 Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI API](https://openai.com/api/)
