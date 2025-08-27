# SupplyGuard AI Integration with OpenRouter

This document explains how to set up and use the AI integration in SupplyGuard using OpenRouter API.

## Overview

SupplyGuard now integrates with OpenRouter API to provide AI-powered supply chain risk analysis. The system uses OpenAI's GPT models through OpenRouter to enhance the analysis capabilities of our AI agents.

## Setup Instructions

### 1. Install Dependencies

```bash
cd supplyguard_backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your OpenRouter API key:
```bash
OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here
```

**Important**: Never commit your actual API key to version control!

### 3. Get OpenRouter API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for an account
3. Generate an API key
4. Add credits to your account for API usage

## Architecture

### AI Service (`src/services/ai_service.py`)
- Central service for AI API calls
- Handles OpenRouter integration
- Provides fallback responses when AI service is unavailable
- Supports multiple analysis types

### Enhanced AI Agents
- **SchedulerAgent**: Analyzes delivery schedule risks
- **PoliticalRiskAgent**: Assesses geopolitical risks
- **LogisticsAgent**: Evaluates transportation risks
- **TariffAgent**: Analyzes trade policy impacts

### Configuration Management (`src/config.py`)
- Centralized configuration management
- Environment variable handling
- Configuration validation

## Usage

### API Endpoints

#### Health Check
```bash
GET /api/v2/ai/health
```
Returns the status of AI services and agents.

#### Natural Language Query
```bash
POST /api/v2/analyze/query
Content-Type: application/json

{
  "query": "What are the schedule risks for equipment delivery?",
  "context": {
    "country": "Germany",
    "equipment_type": "manufacturing"
  }
}
```

#### Specific Agent Analysis
```bash
POST /api/v2/analyze/scheduler
POST /api/v2/analyze/political
POST /api/v2/analyze/logistics
POST /api/v2/analyze/tariff
```

### Testing

Run the integration test script:
```bash
cd supplyguard_backend
python test_ai_integration.py
```

This will test:
- AI service connectivity
- Agent functionality
- API response formatting

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | `sk-or-v1-demo-key-placeholder` |
| `AI_MODEL` | AI model to use | `openai/gpt-3.5-turbo` |
| `AI_TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `AI_MAX_TOKENS` | Maximum response length | `1000` |

### Available Models

Popular models available through OpenRouter:
- `openai/gpt-3.5-turbo` (recommended for cost-effectiveness)
- `openai/gpt-4` (higher quality, more expensive)
- `anthropic/claude-3-haiku` (alternative provider)

## Security Considerations

1. **API Key Protection**: Never expose your API key in code or logs
2. **Environment Variables**: Use `.env` file for local development
3. **Production**: Use secure environment variable management
4. **Rate Limiting**: OpenRouter has rate limits - monitor usage
5. **Cost Control**: Set spending limits in OpenRouter dashboard

## Fallback Behavior

When AI service is unavailable:
- Agents fall back to traditional analysis methods
- System continues to function with reduced capabilities
- Error messages are logged for debugging
- Users receive fallback responses with lower confidence scores

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Check if `OPENROUTER_API_KEY` is set correctly
   - Verify the key is valid and has credits

2. **Model Not Found**
   - Check if the specified model is available
   - Try using `openai/gpt-3.5-turbo` as fallback

3. **Rate Limiting**
   - Reduce request frequency
   - Check OpenRouter dashboard for limits

4. **Network Issues**
   - Verify internet connectivity
   - Check firewall settings

### Debug Mode

Enable debug logging by setting:
```bash
LOG_LEVEL=DEBUG
```

## Cost Management

- Monitor usage in OpenRouter dashboard
- Set spending limits to avoid unexpected charges
- Use cheaper models for development/testing
- Cache responses when appropriate

## Development

### Adding New Analysis Types

1. Add system prompt in `AIService.system_prompts`
2. Create or update agent class
3. Add routing in `AgentOrchestrator`
4. Test with integration script

### Customizing AI Responses

Modify system prompts in `ai_service.py` to adjust:
- Response format
- Analysis focus
- Risk assessment criteria
- Recommendation types

## Support

For issues related to:
- **OpenRouter API**: Check [OpenRouter documentation](https://openrouter.ai/docs)
- **SupplyGuard Integration**: Review logs and test with integration script
- **Configuration**: Verify environment variables and dependencies
