import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
from textblob import TextBlob
import json
from llm_service import LLMService
from config import TOGETHER_API_KEY
from demo_data import get_demo_conversation, get_all_demo_conversations, get_quick_test_conversation

# Initialize LLM Service
@st.cache_resource
def get_llm_service():
    if TOGETHER_API_KEY:
        return LLMService()
    return None

# Configure page
st.set_page_config(
    page_title="LLM Lead Generation Coaching Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .coaching-tip {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #007bff;
        border-left: 6px solid #007bff;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-size: 14px;
        line-height: 1.6;
    }
    .coaching-tip strong {
        color: #007bff;
        font-size: 16px;
        display: block;
        margin-bottom: 8px;
    }
    .coaching-tip em {
        color: #6c757d;
        font-style: italic;
    }
    .lead-score-high {
        background: linear-gradient(90deg, #d4edda, #c3e6cb);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    .lead-score-medium {
        background: linear-gradient(90deg, #fff3cd, #ffeaa7);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    .lead-score-low {
        background: linear-gradient(90deg, #f8d7da, #f5c6cb);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 10px 0;
    }
    .coaching-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        color: white;
    }
    .coaching-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
    }
    .timing-context {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .timing-metric {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        text-align: center;
    }
    .follow-up-optimal {
        background: linear-gradient(90deg, #d4edda, #c3e6cb);
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    .follow-up-good {
        background: linear-gradient(90deg, #fff3cd, #ffeaa7);
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
    }
    .follow-up-delayed {
        background: linear-gradient(90deg, #f8d7da, #f5c6cb);
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

class LeadAnalyzer:
    def __init__(self):
        self.keywords = {
            'interest': ['interested', 'want to know', 'tell me more', 'sounds good', 'impressive'],
            'objection': ['expensive', 'not sure', 'need to think', 'budget', 'competitor'],
            'buying_signals': ['when can we start', 'pricing', 'contract', 'next steps', 'timeline'],
            'pain_points': ['problem', 'challenge', 'struggling', 'difficult', 'issue'],
            'decision_maker': ['I decide', 'my decision', 'I choose', 'I approve', 'final say']
        }
    
    def analyze_conversation(self, text):
        sentiment = TextBlob(text).sentiment
        
        # Count keywords
        keyword_counts = {}
        for category, words in self.keywords.items():
            count = sum(text.lower().count(word.lower()) for word in words)
            keyword_counts[category] = count
        
        # Calculate lead score
        score = self.calculate_lead_score(keyword_counts, sentiment)
        
        # Generate insights
        insights = self.generate_insights(keyword_counts, sentiment, text)
        
        return {
            'sentiment': sentiment,
            'keyword_counts': keyword_counts,
            'lead_score': score,
            'insights': insights,
            'word_count': len(text.split()),
            'engagement_level': self.calculate_engagement(text)
        }
    
    def calculate_lead_score(self, keywords, sentiment):
        base_score = 50
        
        # Sentiment impact
        base_score += sentiment.polarity * 20
        
        # Keyword impact
        base_score += keywords['interest'] * 5
        base_score += keywords['buying_signals'] * 10
        base_score += keywords['decision_maker'] * 8
        base_score -= keywords['objection'] * 3
        
        return max(0, min(100, base_score))
    
    def calculate_engagement(self, text):
        questions = text.count('?')
        exclamations = text.count('!')
        word_count = len(text.split())
        
        if word_count > 100:
            return 'High'
        elif word_count > 50:
            return 'Medium'
        else:
            return 'Low'
    
    def generate_insights(self, keywords, sentiment, text):
        insights = []
        
        if sentiment.polarity > 0.3:
            insights.append("🟢 Positive sentiment detected - prospect is engaged")
        elif sentiment.polarity < -0.1:
            insights.append("🔴 Negative sentiment - address concerns immediately")
        
        if keywords['buying_signals'] > 0:
            insights.append("💰 Buying signals detected - move to proposal stage")
        
        if keywords['objection'] > keywords['interest']:
            insights.append("⚠️ High objection level - focus on value proposition")
        
        if keywords['decision_maker'] > 0:
            insights.append("👑 Decision maker identified - prioritize this lead")
        
        if keywords['pain_points'] > 0:
            insights.append("🎯 Pain points mentioned - align solution benefits")
        
        return insights

def generate_coaching_recommendations(analysis):
    recommendations = []
    
    score = analysis['lead_score']
    sentiment = analysis['sentiment']
    keywords = analysis['keyword_counts']
    
    if score > 80:
        recommendations.append({
            'priority': 'High',
            'action': 'Schedule Demo/Proposal',
            'reason': 'High lead score with strong buying signals'
        })
    elif score > 60:
        recommendations.append({
            'priority': 'Medium',
            'action': 'Send Follow-up with Case Studies',
            'reason': 'Moderate interest, needs nurturing'
        })
    else:
        recommendations.append({
            'priority': 'Low',
            'action': 'Add to Drip Campaign',
            'reason': 'Low engagement, needs long-term nurturing'
        })
    
    if sentiment.polarity < 0:
        recommendations.append({
            'priority': 'High',
            'action': 'Address Concerns Immediately',
            'reason': 'Negative sentiment detected'
        })
    
    if keywords['objection'] > 2:
        recommendations.append({
            'priority': 'High',
            'action': 'Prepare Objection Handling Guide',
            'reason': 'Multiple objections raised'
        })
    
    return recommendations

def create_sample_data():
    """Generate sample lead data for demonstration"""
    np.random.seed(42)
    
    leads_data = []
    companies = ['TechCorp', 'StartupIO', 'Enterprise Solutions', 'Digital Dynamics', 'InnovateLab']
    stages = ['Cold', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed-Won', 'Closed-Lost']
    
    for i in range(50):
        leads_data.append({
            'Lead_ID': f'L{1000+i}',
            'Company': np.random.choice(companies),
            'Lead_Score': np.random.randint(20, 100),
            'Stage': np.random.choice(stages),
            'Days_in_Pipeline': np.random.randint(1, 90),
            'Interactions': np.random.randint(1, 15),
            'Revenue_Potential': np.random.randint(5000, 100000),
            'Source': np.random.choice(['Website', 'LinkedIn', 'Email', 'Referral', 'Cold Call']),
            'Industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail'])
        })
    
    return pd.DataFrame(leads_data)

# Initialize analyzer
analyzer = LeadAnalyzer()

# Sidebar
st.sidebar.title("🎯 Lead Generation Coach")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "Select Tool",
    ["Dashboard", "Conversation Analysis", "Lead Scoring", "Coaching Hub", "Performance Analytics"]
)

# Main Content
if page == "Dashboard":
    st.title("🎯 Lead Generation Dashboard")
    
    # Sample data
    df = create_sample_data()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Total Leads</h3>
            <h2>{}</h2>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        qualified_leads = len(df[df['Stage'].isin(['Qualified', 'Proposal', 'Negotiation'])])
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Qualified Leads</h3>
            <h2>{}</h2>
        </div>
        """.format(qualified_leads), unsafe_allow_html=True)
    
    with col3:
        avg_score = df['Lead_Score'].mean()
        st.markdown("""
        <div class="metric-card">
            <h3>⭐ Avg Lead Score</h3>
            <h2>{:.1f}</h2>
        </div>
        """.format(avg_score), unsafe_allow_html=True)
    
    with col4:
        conversion_rate = len(df[df['Stage'] == 'Closed-Won']) / len(df) * 100
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Conversion Rate</h3>
            <h2>{:.1f}%</h2>
        </div>
        """.format(conversion_rate), unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Lead Score Distribution")
        fig = px.histogram(df, x='Lead_Score', nbins=20, title="Lead Score Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏢 Leads by Industry")
        industry_counts = df['Industry'].value_counts()
        fig = px.pie(values=industry_counts.values, names=industry_counts.index, title="Leads by Industry")
        st.plotly_chart(fig, use_container_width=True)
    
    # Pipeline Analysis
    st.subheader("🔄 Sales Pipeline")
    pipeline_data = df.groupby('Stage').agg({
        'Lead_ID': 'count',
        'Revenue_Potential': 'sum'
    }).reset_index()
    
    fig = px.funnel(pipeline_data, x='Lead_ID', y='Stage', title="Sales Pipeline Funnel")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Conversation Analysis":
    st.title("💬 Conversation Analysis")
    
    st.markdown("""
    Paste your sales conversation below to get AI-powered insights and coaching recommendations.
    """)
    
    # Check if LLM service is available
    llm_service = get_llm_service()
    if not llm_service:
        st.warning("⚠️ Together AI API key not configured. Using basic analysis only.")
    
    # Time Interval Selection
    st.subheader("📅 Conversation Timing")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        conversation_date = st.date_input(
            "Conversation Date",
            value=datetime.now().date(),
            help="Select the date when this conversation took place"
        )
    
    with col2:
        conversation_time = st.time_input(
            "Conversation Time",
            value=datetime.now().time(),
            help="Select the time when this conversation started"
        )
    
    with col3:
        conversation_duration = st.selectbox(
            "Conversation Duration",
            options=["15 minutes", "30 minutes", "45 minutes", "1 hour", "1.5 hours", "2 hours", "2+ hours"],
            index=2,  # Default to 45 minutes
            help="How long did the conversation last?"
        )
    
    # Combine date and time
    conversation_datetime = datetime.combine(conversation_date, conversation_time)
    
    # Display conversation timing info
    st.info(f"""
    📅 **Conversation Details:**
    - **Date:** {conversation_date.strftime('%A, %B %d, %Y')}
    - **Time:** {conversation_time.strftime('%I:%M %p')}
    - **Duration:** {conversation_duration}
    - **Day of Week:** {conversation_date.strftime('%A')}
    """)
    
    # Demo data selection
    st.subheader("🎯 Demo Conversations")
    demo_option = st.selectbox(
        "Choose a demo conversation to test:",
        ["None - Enter my own", "Quick Test", "High-Intent Prospect", "Interested but Hesitant", 
         "Price-Sensitive Lead", "Competitor Comparison", "Future Opportunity", "Objection-Heavy Lead"]
    )
    
    # Load demo conversation if selected
    conversation = ""
    if demo_option == "Quick Test":
        conversation = get_quick_test_conversation()
    elif demo_option != "None - Enter my own":
        demo_key = demo_option.lower().replace(" ", "_").replace("-", "_")
        demo_data = get_demo_conversation(demo_key)
        if demo_data:
            conversation = demo_data["conversation"]
            st.info(f"**Demo: {demo_data['title']}** - Expected Score: {demo_data['expected_score']}")
            with st.expander("Key Insights to Look For"):
                for insight in demo_data["key_insights"]:
                    st.markdown(f"• {insight}")
    
    # Input area
    conversation = st.text_area(
        "Enter Conversation Text:",
        value=conversation,
        height=200,
        placeholder="Paste your sales conversation here..."
    )
    
    if st.button("🔍 Analyze Conversation", type="primary"):
        if conversation:
            with st.spinner("Analyzing conversation with AI..."):
                if llm_service:
                    # Calculate time since conversation
                    time_since = datetime.now() - conversation_datetime
                    hours_since = time_since.total_seconds() / 3600
                    
                    # Prepare timing context
                    timing_context = {
                        'date': conversation_date.strftime('%A, %B %d, %Y'),
                        'time': conversation_time.strftime('%I:%M %p'),
                        'duration': conversation_duration,
                        'day_of_week': conversation_date.strftime('%A'),
                        'time_since': f"{int(hours_since)} hours ago" if hours_since < 24 else f"{int(hours_since / 24)} days ago"
                    }
                    
                    # Calculate follow-up status
                    if hours_since < 24:
                        follow_up_status = "🟢 Optimal"
                    elif hours_since < 72:
                        follow_up_status = "🟡 Good"
                    else:
                        follow_up_status = "🔴 Delayed"
                    
                    # Use LLM-powered analysis with timing context
                    llm_analysis = llm_service.analyze_conversation_llm(conversation, timing_context)
                    llm_score = llm_service.generate_lead_score_llm(llm_analysis)
                    llm_insights = llm_service.generate_insights_llm(conversation, llm_analysis)
                    llm_coaching = llm_service.generate_coaching_recommendations_llm(llm_analysis, llm_score)
                    
                    # Display conversation timing context
                    st.subheader("⏰ Conversation Context")
                    st.markdown("""
                    <div class="timing-context">
                        <div class="timing-metric">
                            <strong>📅 Date:</strong> {date}<br>
                            <strong>🕐 Time:</strong> {time}
                        </div>
                        <div class="timing-metric">
                            <strong>📊 Duration:</strong> {duration}<br>
                            <strong>📅 Day:</strong> {day}
                        </div>
                        <div class="timing-metric">
                            <strong>⏱️ Time Since:</strong> {time_since}<br>
                            <strong>📞 Follow-up:</strong> {follow_up_status}
                        </div>
                    </div>
                    """.format(
                        date=conversation_date.strftime('%m/%d/%Y'),
                        time=conversation_time.strftime('%I:%M %p'),
                        duration=conversation_duration,
                        day=conversation_date.strftime('%A'),
                        time_since=timing_context['time_since'],
                        follow_up_status=follow_up_status
                    ), unsafe_allow_html=True)
                    
                    # Display LLM results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🤖 AI Analysis Results")
                        
                        # Lead Score
                        score = llm_score['overall_score']
                        if score > 70:
                            score_class = "lead-score-high"
                            score_emoji = "🟢"
                        elif score > 40:
                            score_class = "lead-score-medium"
                            score_emoji = "🟡"
                        else:
                            score_class = "lead-score-low"
                            score_emoji = "🔴"
                        
                        st.markdown(f"""
                        <div class="{score_class}">
                            <h3>{score_emoji} Lead Score: {score}/100</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Score breakdown
                        st.subheader("📊 Score Breakdown")
                        breakdown = llm_score['score_breakdown']
                        for category, points in breakdown.items():
                            st.metric(category.replace('_', ' ').title(), f"{points}/25")
                        
                        # Priority and timeline
                        st.metric("🎯 Priority Level", llm_score['priority_level'])
                        st.metric("⏰ Timeline", llm_score['timeline'])
                        st.metric("🎯 Confidence", llm_score['confidence_level'])
                    
                    with col2:
                        st.subheader("🔍 AI Analysis Details")
                        
                        # Sentiment and engagement
                        st.metric("😊 Sentiment Score", f"{llm_analysis['sentiment_score']:.2f}")
                        st.metric("🎯 Engagement Level", llm_analysis['engagement_level'])
                        st.metric("💰 Buying Intent", llm_analysis['buying_intent'])
                        st.metric("🚨 Urgency Level", llm_analysis['urgency_level'])
                        
                        # Key topics
                        if llm_analysis['key_topics']:
                            st.subheader("📝 Key Topics")
                            for topic in llm_analysis['key_topics']:
                                st.markdown(f"• {topic}")
                    
                    # Advanced insights
                    st.subheader("💡 AI-Generated Insights")
                    for insight in llm_insights:
                        st.markdown(f"• {insight}")
                    
                    # Timing insights
                    if llm_analysis.get('timing_insights'):
                        st.subheader("⏰ Timing Insights")
                        for timing_insight in llm_analysis['timing_insights']:
                            st.markdown(f"• {timing_insight}")
                    
                    # Optimal follow-up time
                    if llm_analysis.get('optimal_follow_up_time'):
                        st.subheader("📞 Follow-up Recommendation")
                        optimal_time = llm_analysis['optimal_follow_up_time']
                        if optimal_time == "Immediate":
                            st.success(f"🟢 **{optimal_time}** - Follow up right away while the conversation is fresh!")
                        elif optimal_time in ["Within 24h", "Within 48h"]:
                            st.warning(f"🟡 **{optimal_time}** - Good timing for follow-up")
                        else:
                            st.info(f"🔵 **{optimal_time}** - Plan your follow-up strategy")
                    
                    # Score explanation
                    st.subheader("📋 Score Explanation")
                    st.info(llm_score['score_explanation'])
                    
                    # Coaching Recommendations
                    st.markdown("""
                    <div class="coaching-section">
                        <div class="coaching-header">🎯 AI Coaching Recommendations</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if llm_coaching and len(llm_coaching) > 0:
                        # Check if coaching data is properly formatted
                        if isinstance(llm_coaching, list) and all(isinstance(rec, dict) for rec in llm_coaching):
                            for i, rec in enumerate(llm_coaching, 1):
                                priority_color = {
                                    'High': '🔴',
                                    'Medium': '🟡',
                                    'Low': '🟢',
                                    'Critical': '🚨'
                                }
                                
                                st.markdown(f"""
                                <div class="coaching-tip">
                                    <strong>{priority_color.get(rec.get('priority', 'Medium'), '⚪')} Recommendation #{i}: {rec.get('action', 'Follow up')}</strong>
                                    <em>Category: {rec.get('category', 'General')}</em><br>
                                    <em>Reason: {rec.get('reason', 'Based on conversation analysis')}</em><br>
                                    <strong>Script:</strong> {rec.get('script', 'Schedule a follow-up call to discuss next steps.')}<br>
                                    <em>Timeline: {rec.get('timeline', 'Within 48 hours')}</em><br>
                                    <em>Expected Outcome: {rec.get('expected_outcome', 'Continued engagement')}</em>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            # Handle case where LLM returned a string or malformed data
                            st.warning("⚠️ Coaching recommendations format issue. Using fallback recommendations.")
                            st.info("LLM returned: " + str(type(llm_coaching)) + " - " + str(llm_coaching)[:200] + "...")
                            
                            # Provide fallback recommendations
                            fallback_recommendations = [
                                {
                                    'priority': 'Medium',
                                    'action': 'Schedule Follow-up Call',
                                    'category': 'Follow-up',
                                    'reason': 'Based on conversation analysis',
                                    'script': 'Thank you for your time. Let\'s schedule a follow-up call to discuss your needs in detail.',
                                    'timeline': 'Within 48 hours',
                                    'expected_outcome': 'Continued engagement and deeper discussion'
                                }
                            ]
                            
                            for i, rec in enumerate(fallback_recommendations, 1):
                                st.markdown(f"""
                                <div class="coaching-tip">
                                    <strong>🟡 Recommendation #{i}: {rec['action']}</strong>
                                    <em>Category: {rec['category']}</em><br>
                                    <em>Reason: {rec['reason']}</em><br>
                                    <strong>Script:</strong> {rec['script']}<br>
                                    <em>Timeline: {rec['timeline']}</em><br>
                                    <em>Expected Outcome: {rec['expected_outcome']}</em>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.info("No specific coaching recommendations generated. This might indicate a straightforward conversation or limited data.")
                    
                    # Follow-up email generation
                    if st.button("📧 Generate Follow-up Email"):
                        with st.spinner("Generating personalized email..."):
                            email = llm_service.generate_follow_up_email_llm(conversation, llm_analysis)
                            st.subheader("📧 AI-Generated Follow-up Email")
                            st.text_area("Email Content:", value=email, height=300)
                    
                    # Save analysis option
                    if st.button("💾 Save Analysis"):
                        # Create analysis record
                        analysis_record = {
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'conversation_date': conversation_date.strftime('%Y-%m-%d'),
                            'conversation_time': conversation_time.strftime('%H:%M'),
                            'conversation_duration': conversation_duration,
                            'day_of_week': conversation_date.strftime('%A'),
                            'lead_score': llm_score['overall_score'],
                            'priority_level': llm_score['priority_level'],
                            'timeline': llm_score['timeline'],
                            'confidence_level': llm_score['confidence_level'],
                            'sentiment_score': llm_analysis['sentiment_score'],
                            'engagement_level': llm_analysis['engagement_level'],
                            'buying_intent': llm_analysis['buying_intent'],
                            'urgency_level': llm_analysis['urgency_level'],
                            'optimal_follow_up_time': llm_analysis.get('optimal_follow_up_time', 'Not specified'),
                            'conversation_length': len(conversation),
                            'key_topics': ', '.join(llm_analysis.get('key_topics', [])),
                            'pain_points': ', '.join(llm_analysis.get('pain_points', [])),
                            'objections': ', '.join(llm_analysis.get('objections', [])),
                            'buying_signals': ', '.join(llm_analysis.get('buying_signals', [])),
                            'next_steps': ', '.join(llm_analysis.get('next_steps_suggested', []))
                        }
                        
                        # Save to CSV
                        import os
                        
                        filename = 'conversation_analysis_history.csv'
                        
                        if os.path.exists(filename):
                            # Append to existing file
                            df = pd.read_csv(filename)
                            df = pd.concat([df, pd.DataFrame([analysis_record])], ignore_index=True)
                        else:
                            # Create new file
                            df = pd.DataFrame([analysis_record])
                        
                        df.to_csv(filename, index=False)
                        st.success(f"✅ Analysis saved to {filename}")
                        st.info(f"📊 Total analyses saved: {len(df)}")
                    
                    # View analysis history
                    if st.button("📊 View Analysis History"):
                        import os
                        filename = 'conversation_analysis_history.csv'
                        
                        if os.path.exists(filename):
                            df = pd.read_csv(filename)
                            st.subheader("📊 Conversation Analysis History")
                            
                            # Display summary statistics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Analyses", len(df))
                            with col2:
                                avg_score = df['lead_score'].mean()
                                st.metric("Avg Lead Score", f"{avg_score:.1f}")
                            with col3:
                                recent_analyses = df[df['timestamp'] >= (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')]
                                st.metric("This Week", len(recent_analyses))
                            with col4:
                                high_priority = len(df[df['priority_level'] == 'High'])
                                st.metric("High Priority", high_priority)
                            
                            # Filter options
                            st.subheader("🔍 Filter History")
                            col1, col2 = st.columns(2)
                            with col1:
                                date_filter = st.date_input(
                                    "Filter by Date",
                                    value=datetime.now().date(),
                                    help="Show analyses from this date"
                                )
                            with col2:
                                priority_filter = st.selectbox(
                                    "Filter by Priority",
                                    ["All", "High", "Medium", "Low"]
                                )
                            
                            # Apply filters
                            filtered_df = df.copy()
                            if date_filter:
                                filtered_df = filtered_df[filtered_df['conversation_date'] == date_filter.strftime('%Y-%m-%d')]
                            if priority_filter != "All":
                                filtered_df = filtered_df[filtered_df['priority_level'] == priority_filter]
                            
                            # Display filtered results
                            if len(filtered_df) > 0:
                                st.dataframe(filtered_df[['conversation_date', 'conversation_time', 'conversation_duration', 
                                                        'lead_score', 'priority_level', 'engagement_level', 'optimal_follow_up_time']])
                                
                                # Timing analysis chart
                                st.subheader("⏰ Timing Analysis")
                                fig = px.scatter(filtered_df, x='conversation_time', y='lead_score', 
                                               color='priority_level', size='conversation_length',
                                               title="Lead Score vs Conversation Time",
                                               labels={'conversation_time': 'Time of Day', 'lead_score': 'Lead Score'})
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("No analyses found with the selected filters.")
                        else:
                            st.info("No analysis history found. Save your first analysis to see history here.")
                
                else:
                    # Fallback to original analysis
                    analysis = analyzer.analyze_conversation(conversation)
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Analysis Results")
                    
                    # Lead Score
                    score = analysis['lead_score']
                    if score > 70:
                        score_class = "lead-score-high"
                        score_emoji = "🟢"
                    elif score > 40:
                        score_class = "lead-score-medium"
                        score_emoji = "🟡"
                    else:
                        score_class = "lead-score-low"
                        score_emoji = "🔴"
                    
                    st.markdown(f"""
                    <div class="{score_class}">
                        <h3>{score_emoji} Lead Score: {score:.1f}/100</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Sentiment
                    sentiment = analysis['sentiment']
                    st.metric("😊 Sentiment Score", f"{sentiment.polarity:.2f}")
                    st.metric("🎯 Engagement Level", analysis['engagement_level'])
                    st.metric("📝 Word Count", analysis['word_count'])
                
                with col2:
                    st.subheader("🔍 Keyword Analysis")
                    
                    keywords_df = pd.DataFrame(
                        list(analysis['keyword_counts'].items()),
                        columns=['Category', 'Count']
                    )
                    
                    fig = px.bar(keywords_df, x='Category', y='Count', title="Keyword Categories")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Insights
                st.subheader("💡 Key Insights")
                for insight in analysis['insights']:
                    st.markdown(f"- {insight}")
                
                # Coaching Recommendations
                    st.markdown("""
                    <div class="coaching-section">
                        <div class="coaching-header">🎯 Coaching Recommendations</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                recommendations = generate_coaching_recommendations(analysis)
                    
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        priority_color = {
                            'High': '🔴',
                            'Medium': '🟡',
                            'Low': '🟢'
                        }
                        
                        st.markdown(f"""
                        <div class="coaching-tip">
                            <strong>{priority_color[rec['priority']]} Recommendation #{i}: {rec['action']}</strong><br>
                            <em>{rec['reason']}</em>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No specific coaching recommendations generated for this conversation.")
        else:
            st.warning("Please enter a conversation to analyze.")

elif page == "Lead Scoring":
    st.title("⭐ Lead Scoring System")
    
    st.markdown("""
    Configure and test the lead scoring algorithm based on various factors.
    """)
    
    # Check if LLM service is available
    llm_service = get_llm_service()
    if not llm_service:
        st.warning("⚠️ Together AI API key not configured. Using basic scoring only.")
    
    # AI-Powered Scoring Section
    if llm_service:
        st.subheader("🤖 AI-Powered Lead Scoring")
        
        # Demo conversation selection for AI scoring
        ai_demo_option = st.selectbox(
            "Choose a demo conversation for AI scoring:",
            ["None - Enter my own", "Quick Test", "High-Intent Prospect", "Interested but Hesitant", 
             "Price-Sensitive Lead", "Competitor Comparison", "Future Opportunity", "Objection-Heavy Lead"],
            key="ai_demo"
        )
        
        # Load demo conversation if selected
        ai_conversation = ""
        if ai_demo_option == "Quick Test":
            ai_conversation = get_quick_test_conversation()
        elif ai_demo_option != "None - Enter my own":
            demo_key = ai_demo_option.lower().replace(" ", "_").replace("-", "_")
            demo_data = get_demo_conversation(demo_key)
            if demo_data:
                ai_conversation = demo_data["conversation"]
                st.info(f"**Demo: {demo_data['title']}** - Expected Score: {demo_data['expected_score']}")
        
        ai_conversation = st.text_area(
            "Enter conversation for AI scoring:",
            value=ai_conversation,
            height=150,
            placeholder="Paste conversation text for AI-powered scoring..."
        )
        
        if st.button("🤖 Analyze with AI", type="primary"):
            if ai_conversation:
                with st.spinner("AI is analyzing and scoring..."):
                    # Get AI analysis and scoring
                    ai_analysis = llm_service.analyze_conversation_llm(ai_conversation)
                    ai_score = llm_service.generate_lead_score_llm(ai_analysis)
                    
                    # Display AI results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🤖 AI Score Results")
                        score = ai_score['overall_score']
                        st.metric("AI Lead Score", f"{score}/100")
                        st.metric("Priority Level", ai_score['priority_level'])
                        st.metric("Timeline", ai_score['timeline'])
                        st.metric("Confidence", ai_score['confidence_level'])
                    
                    with col2:
                        st.subheader("📊 AI Score Breakdown")
                        breakdown = ai_score['score_breakdown']
                        for category, points in breakdown.items():
                            st.metric(category.replace('_', ' ').title(), f"{points}/25")
                    
                    # Score explanation
                    st.subheader("📋 AI Score Explanation")
                    st.info(ai_score['score_explanation'])
                    
                    # Recommended action
                    st.subheader("🎯 AI Recommended Action")
                    st.success(ai_score['recommended_action'])
                    
                    # Score interpretation
                    if score > 80:
                        st.success("🔥 Hot Lead - Immediate follow-up required!")
                    elif score > 60:
                        st.warning("🌡️ Warm Lead - Schedule follow-up within 24 hours")
                    elif score > 40:
                        st.info("❄️ Cool Lead - Add to nurture campaign")
                    else:
                        st.error("🧊 Cold Lead - Long-term nurturing required")
            else:
                st.warning("Please enter conversation text for AI analysis.")
        
        st.markdown("---")
    
    # Manual Scoring Configuration
    st.subheader("🔧 Manual Scoring Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Positive Factors:**")
        interest_weight = st.slider("Interest Indicators", 1, 10, 5)
        buying_signals_weight = st.slider("Buying Signals", 1, 10, 8)
        decision_maker_weight = st.slider("Decision Maker", 1, 10, 7)
        engagement_weight = st.slider("Engagement Level", 1, 10, 6)
    
    with col2:
        st.markdown("**Negative Factors:**")
        objection_weight = st.slider("Objections", 1, 10, 3)
        competition_weight = st.slider("Competition Mentions", 1, 10, 2)
        budget_concerns_weight = st.slider("Budget Concerns", 1, 10, 4)
        timing_issues_weight = st.slider("Timing Issues", 1, 10, 3)
    
    # Test Lead Scoring
    st.subheader("🧪 Test Lead Scoring")
    
    test_scenario = st.selectbox(
        "Select Test Scenario:",
        [
            "High-Intent Prospect",
            "Interested but Hesitant",
            "Price-Sensitive Lead",
            "Competitor Comparison",
            "Future Opportunity"
        ]
    )
    
    scenarios = {
        "High-Intent Prospect": {
            "interest": 3,
            "buying_signals": 2,
            "decision_maker": 1,
            "objections": 0,
            "engagement": "High"
        },
        "Interested but Hesitant": {
            "interest": 2,
            "buying_signals": 1,
            "decision_maker": 0,
            "objections": 2,
            "engagement": "Medium"
        },
        "Price-Sensitive Lead": {
            "interest": 1,
            "buying_signals": 0,
            "decision_maker": 1,
            "objections": 3,
            "engagement": "Medium"
        },
        "Competitor Comparison": {
            "interest": 2,
            "buying_signals": 1,
            "decision_maker": 1,
            "objections": 1,
            "engagement": "High"
        },
        "Future Opportunity": {
            "interest": 1,
            "buying_signals": 0,
            "decision_maker": 0,
            "objections": 1,
            "engagement": "Low"
        }
    }
    
    scenario_data = scenarios[test_scenario]
    
    # Calculate score
    base_score = 50
    score = base_score
    score += scenario_data["interest"] * interest_weight
    score += scenario_data["buying_signals"] * buying_signals_weight
    score += scenario_data["decision_maker"] * decision_maker_weight
    score -= scenario_data["objections"] * objection_weight
    
    engagement_bonus = {"High": 10, "Medium": 5, "Low": 0}
    score += engagement_bonus[scenario_data["engagement"]]
    
    score = max(0, min(100, score))
    
    # Display score
    st.metric("Calculated Lead Score", f"{score:.1f}/100")
    
    # Score interpretation
    if score > 80:
        st.success("🔥 Hot Lead - Immediate follow-up required!")
    elif score > 60:
        st.warning("🌡️ Warm Lead - Schedule follow-up within 24 hours")
    elif score > 40:
        st.info("❄️ Cool Lead - Add to nurture campaign")
    else:
        st.error("🧊 Cold Lead - Long-term nurturing required")

elif page == "Coaching Hub":
    st.title("🎓 Coaching Hub")
    
    # Check if LLM service is available
    llm_service = get_llm_service()
    if not llm_service:
        st.warning("⚠️ Together AI API key not configured. Using basic coaching only.")
    
    # AI-Powered Coaching Section
    if llm_service:
        st.subheader("🤖 AI-Powered Coaching")
        
        # Demo conversation selection for coaching
        coaching_demo_option = st.selectbox(
            "Choose a demo conversation for AI coaching:",
            ["None - Enter my own", "Quick Test", "High-Intent Prospect", "Interested but Hesitant", 
             "Price-Sensitive Lead", "Competitor Comparison", "Future Opportunity", "Objection-Heavy Lead"],
            key="coaching_demo"
        )
        
        # Load demo conversation if selected
        coaching_conversation = ""
        if coaching_demo_option == "Quick Test":
            coaching_conversation = get_quick_test_conversation()
        elif coaching_demo_option != "None - Enter my own":
            demo_key = coaching_demo_option.lower().replace(" ", "_").replace("-", "_")
            demo_data = get_demo_conversation(demo_key)
            if demo_data:
                coaching_conversation = demo_data["conversation"]
                st.info(f"**Demo: {demo_data['title']}** - Expected Score: {demo_data['expected_score']}")
        
        coaching_conversation = st.text_area(
            "Enter conversation for AI coaching:",
            value=coaching_conversation,
            height=150,
            placeholder="Paste conversation text for personalized AI coaching..."
        )
        
        if st.button("🤖 Get AI Coaching", type="primary"):
            if coaching_conversation:
                with st.spinner("AI is analyzing and generating coaching recommendations..."):
                    # Get AI analysis and coaching
                    ai_analysis = llm_service.analyze_conversation_llm(coaching_conversation)
                    ai_score = llm_service.generate_lead_score_llm(ai_analysis)
                    ai_coaching = llm_service.generate_coaching_recommendations_llm(ai_analysis, ai_score)
                    
                    # Display AI coaching results
                    st.subheader("🎯 AI Coaching Recommendations")
                    
                    for rec in ai_coaching:
                        priority_color = {
                            'High': '🔴',
                            'Medium': '🟡',
                            'Low': '🟢',
                            'Critical': '🚨'
                        }
                        
                        st.markdown(f"""
                        <div class="coaching-tip">
                            <strong>{priority_color.get(rec['priority'], '⚪')} {rec['action']}</strong><br>
                            <em>Category: {rec['category']}</em><br>
                            <em>Reason: {rec['reason']}</em><br>
                            <strong>Script:</strong> {rec['script']}<br>
                            <em>Timeline: {rec['timeline']}</em><br>
                            <em>Expected Outcome: {rec['expected_outcome']}</em>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Generate follow-up email
                    if st.button("📧 Generate AI Follow-up Email"):
                        with st.spinner("Generating personalized email..."):
                            email = llm_service.generate_follow_up_email_llm(coaching_conversation, ai_analysis)
                            st.subheader("📧 AI-Generated Follow-up Email")
                            st.text_area("Email Content:", email, height=300)
            else:
                st.warning("Please enter conversation text for AI coaching.")
        
        st.markdown("---")
    
    # Traditional Coaching Categories
    st.subheader("📚 Traditional Coaching Resources")
    
    # Coaching Categories
    coaching_categories = {
        "Objection Handling": {
            "tips": [
                "Listen actively to understand the real concern",
                "Acknowledge the objection before responding",
                "Provide specific examples or case studies",
                "Turn objections into questions"
            ],
            "scripts": [
                "Price Objection: 'I understand budget is important. Let me show you the ROI...'",
                "Timing: 'When you say timing, what specifically needs to happen first?'",
                "Competition: 'That's great you're being thorough. What criteria matter most?'"
            ]
        },
        "Discovery Questions": {
            "tips": [
                "Ask open-ended questions",
                "Focus on pain points and impact",
                "Understand decision-making process",
                "Qualify budget and timeline"
            ],
            "scripts": [
                "What's driving you to look for a solution now?",
                "How is this challenge impacting your business?",
                "Walk me through your current process...",
                "What would success look like for you?"
            ]
        },
        "Closing Techniques": {
            "tips": [
                "Use assumptive language",
                "Create urgency appropriately",
                "Address all concerns first",
                "Offer clear next steps"
            ],
            "scripts": [
                "Assumptive: 'When we implement this for you...'",
                "Alternative: 'Would you prefer to start next month or the month after?'",
                "Summary: 'Based on everything we've discussed...'"
            ]
        }
    }
    
    selected_category = st.selectbox("Select Coaching Category:", list(coaching_categories.keys()))
    
    category_data = coaching_categories[selected_category]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Best Practices")
        for tip in category_data["tips"]:
            st.markdown(f"• {tip}")
    
    with col2:
        st.subheader("🗣️ Scripts & Examples")
        for script in category_data["scripts"]:
            st.markdown(f"""
            <div class="coaching-tip">
                {script}
            </div>
            """, unsafe_allow_html=True)
    
    # Practice Session
    st.subheader("🎯 Practice Session")
    
    practice_scenario = st.selectbox(
        "Choose Practice Scenario:",
        [
            "Handling Price Objection",
            "Discovery Call",
            "Closing Presentation",
            "Follow-up Call"
        ]
    )
    
    if st.button("Start Practice Session"):
        st.success(f"Practice session for '{practice_scenario}' would start here.")
        st.info("In a full implementation, this would include role-play scenarios and feedback.")

elif page == "Performance Analytics":
    st.title("📈 Performance Analytics")
    
    # Generate sample performance data
    dates = pd.date_range(start='2025-01-01', end='2025-06-18', freq='D')
    performance_data = []
    
    for date in dates:
        performance_data.append({
            'Date': date,
            'Calls_Made': np.random.randint(5, 25),
            'Emails_Sent': np.random.randint(10, 50),
            'Leads_Generated': np.random.randint(1, 8),
            'Meetings_Booked': np.random.randint(0, 5),
            'Conversion_Rate': np.random.uniform(0.1, 0.4)
        })
    
    perf_df = pd.DataFrame(performance_data)
    
    # Time period selector
    time_period = st.selectbox("Select Time Period:", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
    
    days_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90, "All Time": len(perf_df)}
    filtered_df = perf_df.tail(days_map[time_period])
    
    # Key Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_calls = filtered_df['Calls_Made'].sum()
        st.metric("📞 Total Calls", total_calls)
    
    with col2:
        total_emails = filtered_df['Emails_Sent'].sum()
        st.metric("📧 Total Emails", total_emails)
    
    with col3:
        total_leads = filtered_df['Leads_Generated'].sum()
        st.metric("🎯 Leads Generated", total_leads)
    
    with col4:
        avg_conversion = filtered_df['Conversion_Rate'].mean() * 100
        st.metric("💰 Avg Conversion Rate", f"{avg_conversion:.1f}%")
    
    # Performance Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Daily Activity")
        fig = px.line(filtered_df, x='Date', y=['Calls_Made', 'Emails_Sent'], 
                     title="Daily Outreach Activity")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Lead Generation Trend")
        fig = px.line(filtered_df, x='Date', y='Leads_Generated', 
                     title="Daily Leads Generated")
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance Insights
    st.subheader("🔍 Performance Insights")
    
    # Calculate insights
    best_day = filtered_df.loc[filtered_df['Leads_Generated'].idxmax()]
    avg_leads_per_day = filtered_df['Leads_Generated'].mean()
    
    insights = [
        f"Your best performing day was {best_day['Date'].strftime('%B %d')} with {best_day['Leads_Generated']} leads generated",
        f"Average leads per day: {avg_leads_per_day:.1f}",
        f"Call-to-lead ratio: {total_calls/total_leads:.1f} calls per lead" if total_leads > 0 else "No leads generated yet",
        f"Email-to-lead ratio: {total_emails/total_leads:.1f} emails per lead" if total_leads > 0 else "No leads generated yet"
    ]
    
    for insight in insights:
        st.markdown(f"• {insight}")
    
    # Recommendations
    st.subheader("💡 Recommendations")
    
    if avg_conversion < 0.2:
        st.markdown("""
        <div class="coaching-tip">
            <strong>🎯 Focus on Lead Quality</strong><br>
            Your conversion rate is below 20%. Consider improving lead qualification and targeting.
        </div>
        """, unsafe_allow_html=True)
    
    if total_calls < 100:
        st.markdown("""
        <div class="coaching-tip">
            <strong>📞 Increase Call Volume</strong><br>
            Aim for at least 20 calls per day to maximize lead generation opportunities.
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🚀 **LLM Lead Generation Coaching Tool** - Powered by AI Analytics")
st.markdown("Built with Streamlit • For questions or support, contact your admin")