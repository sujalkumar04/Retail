# Retail AI Agent - Multi-Agent Retail System

A production-ready multi-agent AI system for retail with omnichannel support. Features specialized AI agents for sales, recommendations, inventory, payments, fulfillment, loyalty, and post-purchase support.

## 🌟 Features

- **8 Specialized AI Agents**: Sales, Recommendation, Inventory, Payment, Fulfillment, Loyalty, Post-Purchase
- **Omnichannel Support**: Web, Mobile, WhatsApp, Kiosk, Voice Assistant
- **Real-time Inventory**: Multi-location stock tracking
- **Smart Recommendations**: Personalized product suggestions
- **Loyalty Integration**: Points, tiers, and promotions
- **Streaming Responses**: Real-time AI responses
- **Session Management**: Redis-based conversation persistence

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Redis (optional, falls back to in-memory storage)
- OpenAI API key OR Groq API key (faster, free tier available)

### Installation

1. **Clone and navigate to the project**:
   ```bash
   cd retail-ai-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key:
   # For Groq (recommended - faster, free tier): GROQ_API_KEY=your_key
   # For OpenAI: OPENAI_API_KEY=your_key
   # Set LLM_PROVIDER=groq or openai
   ```

4. **Start Redis** (optional):
   ```bash
   redis-server
   ```

5. **Run the API server**:
   ```bash
   python -m uvicorn api.app:app --reload --port 8000
   ```

6. **Open the web interface**:
   - Open `frontend/index.html` in your browser
   - Or visit `http://localhost:8000` (if serving static files)

## 📁 Project Structure

```
retail-ai-agent/
├── config/              # Configuration and prompts
├── data/                # JSON data files (customers, products, inventory)
├── src/
│   ├── agents/          # AI agents (Sales, Recommendation, etc.)
│   ├── channels/        # Omnichannel implementations
│   ├── models/          # Data models (Customer, Product, Order, etc.)
│   ├── orchestrator/    # Agent routing and workflow
│   ├── services/        # Business logic services
│   └── utils/           # Utilities (LLM client, helpers)
├── api/                 # FastAPI application
│   └── routes/          # API endpoints
├── frontend/            # Web interface
└── tests/               # Test files
```

## 🤖 AI Agents

1. **Sales Agent**: Consultative selling, personalized greetings
2. **Recommendation Agent**: Product suggestions based on preferences
3. **Inventory Agent**: Stock availability, fulfillment options
4. **Payment Agent**: Checkout, payment processing
5. **Fulfillment Agent**: Delivery scheduling, pickup coordination
6. **Loyalty Agent**: Points, promotions, coupons
7. **Post-Purchase Agent**: Order tracking, returns, support

## 📡 API Endpoints

- `POST /api/chat/message` - Send a message
- `POST /api/chat/message/stream` - Send with streaming response
- `GET /api/chat/session/{session_id}` - Get session info
- `GET /health` - Health check

## 🎨 Channels

- **Web Chat**: Rich formatting, images, buttons
- **Mobile App**: Concise messages, quick actions
- **WhatsApp**: Casual tone, emoji support
- **Kiosk**: Large touch targets, clear messaging
- **Voice**: Natural language, SSML support

## 🔧 Configuration

Edit `config/settings.py` or set environment variables:

- `LLM_PROVIDER`: Choose `groq` or `openai` (default: openai)
- `GROQ_API_KEY`: Your Groq API key (get free at console.groq.com)
- `OPENAI_API_KEY`: Your OpenAI API key
- `LLM_MODEL`: 
  - For Groq: `llama-3.3-70b-versatile`, `llama-3.1-70b-versatile`, `mixtral-8x7b-32768`
  - For OpenAI: `gpt-4-turbo-preview`, `gpt-3.5-turbo`
- `REDIS_HOST`: Redis host (default: localhost)
- `STORE_NAME`: Your store name

## 📊 Data Files

- `data/customers.json`: Customer profiles with purchase history
- `data/products.json`: Product catalog
- `data/inventory.json`: Stock levels by location
- `data/promotions.json`: Active promotions and coupons
- `data/loyalty_rules.json`: Loyalty program configuration

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Test specific agent
python -m pytest tests/test_agents.py::test_sales_agent
```

## 🌐 Example Usage

```python
# Using the API
import requests

response = requests.post('http://localhost:8000/api/chat/message', json={
    'message': 'Show me summer dresses under ₹5000',
    'customer_id': 'CUST001',
    'channel': 'web_chat'
})

print(response.json()['response'])
```

## 🔐 Security Notes

- Never commit `.env` file with real API keys
- Use environment variables in production
- Implement proper authentication for production use
- Validate all user inputs

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📧 Support

For issues and questions, please open a GitHub issue.

---

**Built with ❤️ using FastAPI, OpenAI, and modern AI agent patterns**
