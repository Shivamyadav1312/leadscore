# 🧪 Testing Guide - LLM Lead Generation Coaching Tool

This guide will help you test all the features of the application with the provided demo data.

## 🚀 Quick Start Testing

### 1. Start the Application
```bash
streamlit run leadscore.py
```

### 2. Open Your Browser
Navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## 📋 Testing Checklist

### ✅ Basic Functionality Tests

#### Dashboard Page
- [ ] **Load Dashboard**: Verify the dashboard loads with sample data
- [ ] **Key Metrics**: Check that all 4 metric cards display correctly
- [ ] **Charts**: Verify lead score distribution and industry pie chart render
- [ ] **Pipeline Funnel**: Confirm sales pipeline visualization works

#### Conversation Analysis Page
- [ ] **Demo Data Selection**: Test all demo conversation options
- [ ] **Basic Analysis**: Test with fallback analysis (no API key)
- [ ] **AI Analysis**: Test with Together AI API key (if available)
- [ ] **Email Generation**: Test follow-up email generation

#### Lead Scoring Page
- [ ] **Manual Scoring**: Test configurable scoring sliders
- [ ] **Test Scenarios**: Try all 5 predefined scenarios
- [ ] **AI Scoring**: Test AI-powered scoring with demo data
- [ ] **Score Interpretation**: Verify score categories display correctly

#### Coaching Hub Page
- [ ] **Traditional Coaching**: Test static coaching resources
- [ ] **AI Coaching**: Test AI-powered coaching with demo data
- [ ] **Practice Sessions**: Verify practice scenario selection
- [ ] **Email Generation**: Test coaching email generation

#### Performance Analytics Page
- [ ] **Time Period Selection**: Test different time ranges
- [ ] **Metrics Display**: Verify all 4 performance metrics
- [ ] **Charts**: Check activity and lead generation trends
- [ ] **Insights**: Verify performance insights display

## 🎯 Demo Data Testing Scenarios

### 1. High-Intent Prospect Test
**Demo**: "🔥 High-Intent Prospect"
**Expected Score**: High (75-90)
**What to Test**:
- Select "High-Intent Prospect" from demo dropdown
- Click "Analyze Conversation"
- Verify high lead score (70+)
- Check for buying signals and urgency indicators
- Test email generation

**Expected Results**:
- Lead Score: 75-90
- Priority: High/Critical
- Timeline: Immediate/This Week
- Key Insights: Decision maker, urgency, buying signals

### 2. Interested but Hesitant Test
**Demo**: "🤔 Interested but Hesitant"
**Expected Score**: Medium (50-70)
**What to Test**:
- Select "Interested but Hesitant" from demo dropdown
- Analyze conversation
- Check for objections and concerns
- Verify medium priority recommendations

**Expected Results**:
- Lead Score: 50-70
- Priority: Medium
- Timeline: This Week/This Month
- Key Insights: Objections, budget concerns, manager approval needed

### 3. Price-Sensitive Lead Test
**Demo**: "💰 Price-Sensitive Lead"
**Expected Score**: Low-Medium (30-50)
**What to Test**:
- Select "Price-Sensitive Lead" from demo dropdown
- Analyze conversation
- Check for price objections
- Verify budget constraints identified

**Expected Results**:
- Lead Score: 30-50
- Priority: Low/Medium
- Timeline: This Month/Long-term
- Key Insights: Price sensitivity, comparing alternatives

### 4. Competitor Comparison Test
**Demo**: "🏆 Competitor Comparison"
**Expected Score**: Medium-High (60-80)
**What to Test**:
- Select "Competitor Comparison" from demo dropdown
- Analyze conversation
- Check for competitive analysis
- Verify timeline pressure

**Expected Results**:
- Lead Score: 60-80
- Priority: Medium/High
- Timeline: This Week/This Month
- Key Insights: Competitor evaluation, timeline pressure

### 5. Future Opportunity Test
**Demo**: "⏰ Future Opportunity"
**Expected Score**: Low (20-40)
**What to Test**:
- Select "Future Opportunity" from demo dropdown
- Analyze conversation
- Check for long timeline
- Verify nurture campaign recommendations

**Expected Results**:
- Lead Score: 20-40
- Priority: Low
- Timeline: Long-term
- Key Insights: Future need, nurture campaign

### 6. Objection-Heavy Lead Test
**Demo**: "🚫 Objection-Heavy Lead"
**Expected Score**: Very Low (10-25)
**What to Test**:
- Select "Objection-Heavy Lead" from demo dropdown
- Analyze conversation
- Check for multiple objections
- Verify low priority recommendations

**Expected Results**:
- Lead Score: 10-25
- Priority: Low
- Timeline: Long-term
- Key Insights: Multiple objections, resistance to change

## 🤖 AI Features Testing (Requires API Key)

### Prerequisites
1. Get Together AI API key from [together.ai](https://together.ai/)
2. Create `.env` file with: `TOGETHER_API_KEY=your_key_here`
3. Restart the application

### AI Testing Scenarios

#### 1. AI Conversation Analysis
- Select any demo conversation
- Click "Analyze Conversation"
- Verify AI-generated insights appear
- Check for detailed score breakdown
- Test AI coaching recommendations

#### 2. AI Lead Scoring
- Go to Lead Scoring page
- Select demo conversation for AI scoring
- Click "Analyze with AI"
- Verify AI score explanation
- Check for detailed breakdown

#### 3. AI Coaching
- Go to Coaching Hub page
- Select demo conversation for AI coaching
- Click "Get AI Coaching"
- Verify personalized recommendations
- Test AI email generation

#### 4. AI Insights
- Test conversation analysis
- Check for AI-generated insights
- Verify insights are relevant and actionable

## 🔧 Fallback Testing (No API Key)

### Test Fallback Functionality
1. Remove or comment out API key in `.env`
2. Restart application
3. Test all features with demo data
4. Verify fallback analysis works
5. Check that basic functionality remains

**Expected Fallback Behavior**:
- Basic keyword analysis instead of AI
- Standard scoring algorithms
- Pre-defined coaching recommendations
- Generic email templates

## 📊 Performance Testing

### Load Testing
- Test with long conversations (1000+ words)
- Test with multiple rapid analyses
- Verify UI responsiveness
- Check memory usage

### Error Handling
- Test with empty conversation text
- Test with invalid API key
- Test with network issues
- Verify graceful error messages

## 🎨 UI/UX Testing

### Responsive Design
- Test on different screen sizes
- Verify mobile compatibility
- Check sidebar functionality
- Test navigation between pages

### Visual Elements
- Verify all emojis display correctly
- Check color-coded score indicators
- Test chart responsiveness
- Verify custom CSS styling

## 🐛 Common Issues & Solutions

### Issue: "API key not found"
**Solution**: Create `.env` file with your Together AI API key

### Issue: "Module not found"
**Solution**: Run `pip install -r requirements.txt`

### Issue: Charts not displaying
**Solution**: Check internet connection for Plotly CDN

### Issue: Slow performance
**Solution**: Use smaller models in `config.py`

### Issue: Demo data not loading
**Solution**: Check `demo_data.py` file exists and is properly formatted

## 📈 Success Criteria

### ✅ All Tests Pass When:
- [ ] All demo conversations load correctly
- [ ] Analysis produces expected scores
- [ ] Charts and visualizations render
- [ ] AI features work (with API key)
- [ ] Fallback features work (without API key)
- [ ] Email generation functions
- [ ] UI is responsive and user-friendly
- [ ] No critical errors in console

### 🎯 Performance Targets:
- Page load time: < 3 seconds
- Analysis response time: < 10 seconds
- AI response time: < 30 seconds
- Memory usage: < 500MB

## 📝 Testing Report Template

After completing tests, document:

```
Test Date: [Date]
Tester: [Name]
Environment: [OS, Browser, etc.]

✅ Passed Tests:
- [List passed tests]

❌ Failed Tests:
- [List failed tests with details]

🐛 Issues Found:
- [List any bugs or issues]

💡 Recommendations:
- [Suggestions for improvement]

Overall Status: [Pass/Fail]
```

## 🚀 Ready to Launch!

Once all tests pass, your application is ready for production use!

**Next Steps**:
1. Deploy to your preferred platform
2. Set up monitoring and logging
3. Train users on the new features
4. Monitor performance and usage

---

**Happy Testing! 🎉** 