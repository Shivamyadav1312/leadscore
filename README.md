# LLM Lead Generation Coaching Tool

A comprehensive AI-powered sales coaching and lead generation tool built with Streamlit and Together AI.

## 🚀 Features

### 🤖 AI-Powered Analysis
- **Conversation Analysis**: Advanced sentiment and intent analysis using LLMs
- **Lead Scoring**: Intelligent scoring based on multiple factors
- **Coaching Recommendations**: Personalized coaching suggestions
- **Follow-up Email Generation**: AI-generated personalized emails
- **Insights Generation**: Deep insights from conversation patterns

### 📊 Traditional Features
- **Dashboard**: Key metrics and performance tracking
- **Lead Scoring**: Configurable scoring algorithms
- **Coaching Hub**: Best practices and scripts
- **Performance Analytics**: Activity tracking and insights

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Together AI API Key

#### Option A: Environment Variable
Create a `.env` file in the project root:
```env
TOGETHER_API_KEY=your_together_ai_api_key_here
TOGETHER_MODEL=llama-3.1-8b-instant
```

#### Option B: System Environment Variable
```bash
# Windows
set TOGETHER_API_KEY=your_together_ai_api_key_here

# macOS/Linux
export TOGETHER_API_KEY=your_together_ai_api_key_here
```

### 3. Get Together AI API Key
1. Visit [Together AI](https://together.ai/)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your environment

### 4. Run the Application
```bash
streamlit run leadscore.py
```

## 🎯 How to Use

### Conversation Analysis
1. Navigate to "Conversation Analysis"
2. Paste your sales conversation
3. Click "Analyze Conversation with AI"
4. Review AI-generated insights, scoring, and recommendations
5. Generate personalized follow-up emails

### AI-Powered Lead Scoring
1. Go to "Lead Scoring"
2. Enter conversation text in the AI section
3. Get comprehensive scoring with breakdown
4. Review AI explanations and recommendations

### AI Coaching
1. Visit "Coaching Hub"
2. Input conversation for personalized coaching
3. Receive AI-generated recommendations
4. Get specific scripts and timelines

## 🔧 Configuration

### Model Settings
Edit `config.py` to customize:
- Model selection for different tasks
- Temperature and other parameters
- API configuration

### Available Models
- `llama-3.1-8b-instant` (default)
- `llama-3.1-70b-instant`
- `mixtral-8x7b-instant`
- `qwen2.5-32b-instant`

## 📁 Project Structure

```
leadscore/
├── leadscore.py          # Main Streamlit application
├── llm_service.py        # Together AI service layer
├── config.py             # Configuration and settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .env                 # Environment variables (create this)
```

## 🤖 LLM Features Explained

### Conversation Analysis
The AI analyzes conversations for:
- **Sentiment Score**: Emotional tone (-1 to 1)
- **Engagement Level**: Low/Medium/High
- **Buying Intent**: Purchase likelihood
- **Key Topics**: Main discussion points
- **Pain Points**: Customer challenges
- **Objections**: Concerns and hesitations
- **Buying Signals**: Positive indicators
- **Decision Maker Indicators**: Authority signals
- **Urgency Level**: Timeline pressure
- **Risk Factors**: Potential issues

### Lead Scoring
Comprehensive scoring based on:
- **Buying Intent** (0-25 points)
- **Decision Power** (0-20 points)
- **Urgency** (0-15 points)
- **Budget Availability** (0-15 points)
- **Fit Score** (0-15 points)
- **Engagement** (0-10 points)

### Coaching Recommendations
AI generates personalized recommendations with:
- **Priority Level**: Critical/High/Medium/Low
- **Category**: Objection Handling/Discovery/Closing/Follow-up
- **Specific Actions**: What to do next
- **Scripts**: Sample language to use
- **Timeline**: When to implement
- **Expected Outcomes**: What to expect

## 🔄 Fallback System

The application includes robust fallback mechanisms:
- If LLM analysis fails, falls back to basic keyword analysis
- Graceful error handling with user-friendly messages
- Maintains functionality even without API access

## 🚨 Troubleshooting

### API Key Issues
- Ensure `TOGETHER_API_KEY` is set correctly
- Check API key permissions and quota
- Verify internet connection

### Model Issues
- Try different models in `config.py`
- Adjust temperature and other parameters
- Check Together AI service status

### Performance Issues
- Use smaller models for faster responses
- Reduce `max_tokens` in configuration
- Consider caching for repeated analyses

## 📈 Future Enhancements

- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Custom model fine-tuning
- [ ] Real-time conversation analysis
- [ ] Integration with video/audio calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Together AI documentation
3. Open an issue on GitHub

---

**Built with ❤️ using Streamlit and Together AI** 