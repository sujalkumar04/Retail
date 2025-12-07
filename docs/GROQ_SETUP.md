# Groq API Integration Guide

## What is Groq?

Groq provides ultra-fast LLM inference with a generous free tier. It's an excellent alternative to OpenAI for development and production use.

**Benefits:**
- ⚡ **10x faster** inference than OpenAI
- 🆓 **Free tier** with generous limits
- 🎯 **Same API interface** as OpenAI
- 🚀 **Production-ready** models (Llama 3.3, Mixtral)

## Setup Instructions

### 1. Get Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys
4. Create a new API key

### 2. Configure the Application

Edit your `.env` file:

```bash
# Set Groq as the provider
LLM_PROVIDER=groq

# Add your Groq API key
GROQ_API_KEY=gsk_your_groq_api_key_here

# Choose a model (recommended)
LLM_MODEL=llama-3.3-70b-versatile

# Temperature (0.0 - 2.0)
LLM_TEMPERATURE=0.7
```

### 3. Available Models

**Recommended Models:**
- `llama-3.3-70b-versatile` - Latest Llama 3.3, best quality
- `llama-3.1-70b-versatile` - Llama 3.1, very fast
- `mixtral-8x7b-32768` - Mixtral, good for long contexts

**All models support:**
- Streaming responses
- Function calling
- JSON mode
- Large context windows

### 4. Restart the Server

After updating `.env`, restart the server:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
python -m uvicorn api.app:app --reload --port 8000
```

## Switching Between Providers

You can easily switch between Groq and OpenAI by changing the `LLM_PROVIDER` in `.env`:

```bash
# Use Groq (fast, free)
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile

# Or use OpenAI (more expensive)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
```

## Performance Comparison

| Provider | Model | Speed | Cost | Quality |
|----------|-------|-------|------|---------|
| Groq | llama-3.3-70b | ⚡⚡⚡⚡⚡ | Free | ⭐⭐⭐⭐ |
| Groq | mixtral-8x7b | ⚡⚡⚡⚡⚡ | Free | ⭐⭐⭐⭐ |
| OpenAI | gpt-4-turbo | ⚡⚡ | $$$ | ⭐⭐⭐⭐⭐ |
| OpenAI | gpt-3.5-turbo | ⚡⚡⚡ | $ | ⭐⭐⭐ |

## Troubleshooting

### "Groq client not available"
Install the groq package:
```bash
pip install groq==0.11.0
```

### Rate Limits
Groq free tier limits:
- 30 requests per minute
- 14,400 requests per day

For production, consider upgrading to a paid plan.

## Example Usage

The integration is transparent - no code changes needed! Just set the environment variables and the system automatically uses Groq:

```python
# The LLM client automatically uses Groq when configured
from src.utils.llm_client import LLMClient

client = LLMClient()  # Uses Groq if LLM_PROVIDER=groq
response = client.generate(messages=[...])
```

## Links

- [Groq Console](https://console.groq.com)
- [Groq Documentation](https://console.groq.com/docs)
- [Groq Pricing](https://wow.groq.com/pricing)
