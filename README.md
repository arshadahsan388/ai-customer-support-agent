# AI-Powered Customer Support Agent

An intelligent customer support system built with LangGraph that automatically processes support tickets through classification, knowledge base retrieval, AI response generation, and quality review.

## 🎥 Demo Video

Watch the demo walkthrough of this AI-powered customer support agent:

[![AI Support Agent Demo](https://img.youtube.com/vi/nEdmqNW9P8A/0.jpg)](https://youtu.be/nEdmqNW9P8A)

[🔗 View on YouTube](https://www.youtube.com/watch?v=nEdmqNW9P8A)

## 🚀 Features

- **Automated Classification**: Intelligently categorizes support tickets into Billing, Technical, Security, or General categories
- **Knowledge Base Integration**: Searches predefined solutions using keyword matching and semantic similarity
- **AI Response Generation**: Creates personalized responses using Google's Gemini AI when knowledge base solutions are insufficient
- **Quality Review System**: Automatically reviews generated responses for clarity, completeness, and professionalism
- **Smart Escalation**: Automatically escalates complex issues to human agents with detailed logging
- **Retry Logic**: Improves responses through iterative refinement with configurable retry limits

## 📋 System Requirements

- Python 3.8 or higher
- Google Gemini API key
- 4GB RAM minimum
- Internet connection for AI model access

## 🛠️ Setup Instructions

### 1. Clone or Download the Project

```bash
# If using git
git clone https://github.com/arshadahsan388/ai-customer-support-agent.git
cd ai-customer-support-agent

# Or download and extract the project files
```

### 2. Set Up Python Environment

#### Option A: Using Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv support_agent_env

# Activate virtual environment
# On Windows:
support_agent_env\Scripts\activate
# On macOS/Linux:
source support_agent_env/bin/activate
```

#### Option B: Using Conda
```bash
# Create conda environment
conda create -n support_agent python=3.9
conda activate support_agent
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

#### Option A: Environment Variable (Recommended)
```bash
# Set environment variable
export GEMINI_API_KEY="your_gemini_api_key_here"

# On Windows Command Prompt:
set GEMINI_API_KEY=your_gemini_api_key_here

# On Windows PowerShell:
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

#### Option B: Update Configuration File
Edit `config.py` and replace the placeholder API key:
```python
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

### 5. Verify Installation

```bash
python main.py --health-check
```

## 🎯 How to Run the Agent

### Basic Usage

```bash
# Process a single support ticket
python main.py --subject "Billing issue" --description "I was charged twice"

# Run with debug information
python main.py --subject "Password help" --description "I can't reset my password" --debug
```

### Interactive Mode

```bash
# Start interactive session
python main.py --interactive
```

This will prompt you to enter support requests interactively:
```
Subject: I was charged twice
Description: I see duplicate charges on my credit card
```

### Test Scenarios

```bash
# Run predefined test cases
python main.py --test
```

### Default Example

```bash
# Run the default billing example
python main.py
```

## 🏗️ Architecture & Design Decisions

### System Architecture

The support agent follows a **workflow-based architecture** using LangGraph, which provides:

1. **Stateful Processing**: Each support ticket maintains state throughout the workflow
2. **Conditional Routing**: Different paths based on review results and escalation needs
3. **Retry Logic**: Automatic improvement iterations for better responses
4. **Error Handling**: Graceful degradation and escalation on failures

### Workflow Diagram

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  CLASSIFY   │───▶│   RETRIEVE   │───▶│ AUTO_AGENT  │
│  (Category) │    │ (Knowledge   │    │ (AI Response│
│             │    │    Base)     │    │ Generation) │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  DECISION   │◀───│    REVIEW    │◀───│             │
│ (Continue/  │    │ (Quality     │    │             │
│    End)     │    │   Check)     │    │             │
└─────────────┘    └──────────────┘    └─────────────┘
      │                    │
      │ (if needs          │ (if approved)
      │  improvement)      │
      ▼                    ▼
┌─────────────┐         ┌─────┐
│   RETRY     │         │ END │
│ (Back to    │         │     │
│  Retrieve)  │         │     │
└─────────────┘         └─────┘
```

### Key Design Decisions

#### 1. **Modular Node Architecture**
- **Rationale**: Each processing step is isolated in its own module for maintainability
- **Benefits**: Easy testing, debugging, and feature additions
- **Implementation**: Separate files in `/nodes` directory with clear interfaces

#### 2. **Knowledge Base Design**
- **Rationale**: Structured knowledge base with categories, keywords, and IDs
- **Benefits**: Fast retrieval, easy maintenance, and expandability
- **Implementation**: Keyword-based matching with similarity fallback

#### 3. **Multi-Strategy Search**
```python
# Search priorities:
1. Keyword matching (highest precision)
2. Category-based filtering (contextual relevance)  
3. Similarity matching (fallback coverage)
```

#### 4. **Quality Review System**
- **Rationale**: Ensure professional, helpful responses before delivery
- **Benefits**: Consistent quality, reduced human oversight needed
- **Implementation**: AI-powered review with manual quality checks

#### 5. **Smart Escalation Logic**
```python
# Escalation triggers:
- Maximum retry attempts exceeded
- AI unable to generate adequate response
- Response indicates human intervention needed
- System errors or failures
```

#### 6. **Stateful Processing**
- **Rationale**: Maintain context across workflow steps for better responses
- **Benefits**: Personalized responses, retry capability, audit trail
- **Implementation**: TypedDict state management with validation

#### 7. **Error Handling Strategy**
- **Graceful Degradation**: System continues operation even with component failures
- **Automatic Escalation**: Failed processing automatically escalates to humans
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

### Technology Stack

| Component | Technology | Reasoning |
|-----------|------------|-----------|
| **Workflow Engine** | LangGraph | State management, conditional routing, retry logic |
| **AI Model** | Google Gemini | High-quality text generation, cost-effective |
| **Language Framework** | LangChain | AI integration, prompt management |
| **State Management** | TypedDict | Type safety, validation, IDE support |
| **Logging** | Python logging | Debugging, monitoring, audit trails |
| **Configuration** | Python modules | Environment-based config, easy deployment |

## 📁 Project Structure

```
support_agent/
├── main.py                 # Entry point and CLI interface
├── graph.py               # LangGraph workflow definition
├── config.py              # Configuration and settings
├── state.py               # State management and validation
├── utils.py               # Utility functions and helpers
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── escalation_log.csv    # Escalated tickets log
├── support_agent.log     # Application logs
└── nodes/                # Workflow processing nodes
    ├── __init__.py
    ├── classify.py       # Ticket classification
    ├── retrieve.py       # Knowledge base search
    ├── auto_agent.py     # AI response generation
    ├── review.py         # Quality review
    ├── should_continue.py # Workflow decisions
    └── knowledge_base.py  # Knowledge base data
```

## 📊 Configuration Options

### System Configuration (`config.py`)

```python
# Model settings
MODEL_CONFIG = {
    "model_name": "gemini-1.5-flash",  # AI model to use
    "temperature": 0.3,                # Response creativity (0-1)
    "max_tokens": 1000                 # Maximum response length
}

# System behavior
SYSTEM_CONFIG = {
    "max_retry_attempts": 2,           # Maximum processing retries
    "similarity_threshold": 0.4,       # Minimum similarity for matches
    "escalation_log_path": "escalation_log.csv"  # Escalation log file
}
```

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

## 🧪 Testing

### Run Health Checks
```bash
python main.py --health-check
```

### Run Test Scenarios
```bash
python main.py --test
```

### Test Individual Components
```python
# Test classification
from nodes.classify import classify_node
result = classify_node({"subject": "test", "description": "billing issue"})

# Test knowledge base
from nodes.retrieve import retrieve_node
result = retrieve_node({"description": "I was charged twice"})
```

## 📈 Performance Considerations

### Response Times
- **Knowledge Base Retrieval**: ~100-500ms
- **AI Response Generation**: ~2-5 seconds
- **Quality Review**: ~1-3 seconds
- **Total Processing**: ~5-10 seconds per ticket

### Scalability
- **Concurrent Processing**: LangGraph supports async execution
- **Knowledge Base**: In-memory for fast access (scalable to databases)
- **API Rate Limits**: Respects Gemini API rate limits

### Cost Optimization
- **Knowledge Base First**: Reduces AI API calls for common issues
- **Efficient Prompts**: Optimized prompts minimize token usage
- **Smart Retry**: Limited retries prevent excessive API calls

## 🔍 Monitoring and Logging

### Log Files
- `support_agent.log`: Application logs with timestamps
- `escalation_log.csv`: Escalated tickets with details

### Key Metrics to Monitor
- Response accuracy rate
- Escalation rate
- Average processing time
- Knowledge base hit rate

## 🚀 Deployment Considerations

### Development Environment
```bash
# Install development dependencies
pip install -r requirements.txt
python main.py --health-check
```

### Production Environment
1. **Environment Variables**: Use secure environment variable management
2. **Logging**: Configure log rotation and monitoring
3. **Error Tracking**: Integrate with error tracking services
4. **Rate Limiting**: Implement API rate limiting
5. **Database**: Replace in-memory knowledge base with database
6. **Authentication**: Add API authentication for production use

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 🔧 Customization

### Adding New Knowledge Base Entries
Edit `nodes/knowledge_base.py`:
```python
{
    "id": "new_001",
    "category": "Technical",
    "question": "How do I update my profile?",
    "keywords": ["update profile", "edit account", "change information"],
    "answer": "Go to Settings > Profile and click Edit."
}
```

### Modifying AI Prompts
Update prompts in respective node files:
- Classification: `nodes/classify.py`
- AI Response: `nodes/auto_agent.py`
- Quality Review: `nodes/review.py`

### Changing Workflow Logic
Modify `graph.py` to add/remove nodes or change routing logic.

## 🐛 Troubleshooting

### Common Issues

#### API Key Issues
```
Error: API key not found
Solution: Set GEMINI_API_KEY environment variable
```

#### Import Errors
```
Error: No module named 'langgraph'
Solution: pip install -r requirements.txt
```

#### Permission Errors
```
Error: Permission denied writing to escalation_log.csv
Solution: Check file permissions or run with appropriate privileges
```

### Debug Mode
Run with debug flag for detailed information:
```bash
python main.py --debug --subject "test" --description "test issue"
```

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

---

**Need Help?** Run `python main.py --help` for command-line options or `python main.py --health-check` to verify system health.
