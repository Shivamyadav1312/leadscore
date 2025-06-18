import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
from textblob import TextBlob
import json

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
        background: #f0f8ff;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .lead-score-high {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .lead-score-medium {
        background: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .lead-score-low {
        background: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
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
    
    # Input area
    conversation = st.text_area(
        "Enter Conversation Text:",
        height=200,
        placeholder="Paste your sales conversation here..."
    )
    
    if st.button("🔍 Analyze Conversation", type="primary"):
        if conversation:
            with st.spinner("Analyzing conversation..."):
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
                st.subheader("🎯 Coaching Recommendations")
                recommendations = generate_coaching_recommendations(analysis)
                
                for rec in recommendations:
                    priority_color = {
                        'High': '🔴',
                        'Medium': '🟡',
                        'Low': '🟢'
                    }
                    
                    st.markdown(f"""
                    <div class="coaching-tip">
                        <strong>{priority_color[rec['priority']]} {rec['action']}</strong><br>
                        <em>{rec['reason']}</em>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Please enter a conversation to analyze.")

elif page == "Lead Scoring":
    st.title("⭐ Lead Scoring System")
    
    st.markdown("""
    Configure and test the lead scoring algorithm based on various factors.
    """)
    
    # Scoring Configuration
    st.subheader("🔧 Scoring Configuration")
    
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