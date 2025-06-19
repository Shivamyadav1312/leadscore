#!/usr/bin/env python3
"""
Demo data for testing the LLM Lead Generation Coaching Tool
"""

# Sample sales conversations for testing
DEMO_CONVERSATIONS = {
    "high_intent_prospect": {
        "title": "🔥 High-Intent Prospect",
        "conversation": """
        Sales Rep: Hi John, thanks for taking the time to speak with me today. I understand you're looking for a CRM solution for your growing sales team.

        Prospect: Yes, absolutely. We're currently using spreadsheets and it's becoming a nightmare. We have 15 salespeople and we're losing deals because we can't track follow-ups properly.

        Sales Rep: That's a common challenge. Can you tell me more about your current process and what specific pain points you're experiencing?

        Prospect: Well, we're missing follow-ups, deals are falling through the cracks, and our sales manager can't get a clear picture of our pipeline. We need something that can automate follow-ups and give us better visibility.

        Sales Rep: I see. And what's your timeline for implementing a solution?

        Prospect: We need this ASAP. Our Q4 targets are at risk, and I'm the one who makes the final decision on this. What's your pricing like?

        Sales Rep: Our enterprise plan is $99 per user per month, which includes all the automation features you mentioned. We can get you set up within 2 weeks.

        Prospect: That sounds reasonable. Can you send me a proposal? I'd like to see the ROI calculation and implementation timeline.

        Sales Rep: Absolutely. I'll prepare a detailed proposal with ROI analysis and send it to you by end of day. When would be a good time to schedule a demo for your team?

        Prospect: How about next Tuesday at 2 PM? I'll get the team together.
        """,
        "expected_score": "High (75-90)",
        "key_insights": [
            "Strong buying signals (timeline, decision maker, pricing question)",
            "Clear pain points identified",
            "Urgency expressed (Q4 targets at risk)",
            "Decision maker confirmed"
        ]
    },
    
    "interested_but_hesitant": {
        "title": "🤔 Interested but Hesitant",
        "conversation": """
        Sales Rep: Hi Sarah, thanks for the call. I understand you downloaded our whitepaper on sales automation.

        Prospect: Yes, it was interesting. We're looking at different options for improving our sales process.

        Sales Rep: Great! Can you tell me more about what you're currently using and what you're hoping to achieve?

        Prospect: We have a basic CRM, but it's not really helping us close more deals. We're considering a few different solutions.

        Sales Rep: What specific challenges are you facing with your current setup?

        Prospect: Well, our team isn't really using it consistently, and we're not sure if it's the right fit for our workflow. Plus, we're concerned about the cost and implementation time.

        Sales Rep: I understand those concerns. What's your team size and what's your budget range?

        Prospect: We have 8 salespeople, and we're looking to spend around $5,000-$7,000 annually. But we need to see clear ROI.

        Sales Rep: That's definitely achievable with our solution. Would you be interested in a free trial to see how it works with your team?

        Prospect: Maybe. I need to think about it and discuss with my manager first. Can you send me some information?

        Sales Rep: Of course. I'll send you a detailed overview and some case studies. When would be a good time to follow up?

        Prospect: Give me a couple of weeks to review everything.
        """,
        "expected_score": "Medium (50-70)",
        "key_insights": [
            "Interest shown but multiple objections",
            "Budget constraints mentioned",
            "Need for manager approval",
            "Timeline extended (couple of weeks)"
        ]
    },
    
    "price_sensitive_lead": {
        "title": "💰 Price-Sensitive Lead",
        "conversation": """
        Sales Rep: Hi Mike, thanks for your interest in our sales automation platform.

        Prospect: Hi. I saw your ad and wanted to learn more about pricing.

        Sales Rep: Sure! Can you tell me a bit about your business and what you're looking to achieve?

        Prospect: We're a small startup with 5 salespeople. We need something affordable but effective.

        Sales Rep: What's your current sales process like?

        Prospect: We're using Google Sheets and email. It's not ideal, but we can't afford expensive enterprise solutions.

        Sales Rep: I understand budget is important. Our starter plan is $29 per user per month. What's your budget range?

        Prospect: That's still more than we were hoping to spend. We were thinking more like $15-20 per user. Do you have any discounts for startups?

        Sales Rep: We do offer a 20% discount for startups under 2 years old. That would bring it down to about $23 per user.

        Prospect: That's better, but I'm still not sure. We're also looking at some free alternatives. What makes your solution worth the extra cost?

        Sales Rep: Great question. Our platform includes AI-powered lead scoring, automated follow-ups, and advanced analytics that free solutions don't offer. Would you like to see a demo?

        Prospect: Maybe. I need to compare with other options first. Can you send me pricing for all your plans?

        Sales Rep: Absolutely. I'll send that over right away. When would be a good time to follow up?

        Prospect: I'll let you know when I've made a decision.
        """,
        "expected_score": "Low-Medium (30-50)",
        "key_insights": [
            "Strong price sensitivity",
            "Comparing with free alternatives",
            "Small team size",
            "No immediate urgency"
        ]
    },
    
    "competitor_comparison": {
        "title": "🏆 Competitor Comparison",
        "conversation": """
        Sales Rep: Hi Jennifer, thanks for taking the time to speak with me about our sales platform.

        Prospect: Hi. We're evaluating several CRM solutions, including yours and Salesforce.

        Sales Rep: Excellent! What criteria are you using to evaluate the different options?

        Prospect: We need something that integrates with our existing tools, has good mobile support, and provides detailed reporting. We're also concerned about implementation complexity.

        Sales Rep: Those are important factors. Can you tell me more about your current tech stack and what integrations are most critical?

        Prospect: We use Slack, Gmail, and QuickBooks. Salesforce seems to have more integrations, but your platform looks more user-friendly.

        Sales Rep: That's a great observation. While Salesforce has more integrations, our platform is designed specifically for ease of use and quick implementation. What's your timeline for making a decision?

        Prospect: We need to decide within the next month. Our current contract expires in 6 weeks.

        Sales Rep: Perfect timing. We can have you up and running within 2 weeks. What's your team size and who else is involved in the decision?

        Prospect: We have 12 salespeople, and I'm the primary decision maker, but I need to get final approval from our CFO.

        Sales Rep: Understood. Would you be interested in a side-by-side comparison with Salesforce, focusing on the specific features that matter most to you?

        Prospect: That would be very helpful. Can you also provide some customer references?

        Sales Rep: Absolutely. I'll prepare a detailed comparison and connect you with some of our customers in your industry. When would be a good time for a demo?

        Prospect: How about next Thursday at 10 AM?
        """,
        "expected_score": "Medium-High (60-80)",
        "key_insights": [
            "Comparing with major competitor (Salesforce)",
            "Clear evaluation criteria",
            "Timeline pressure (contract expiring)",
            "Decision maker identified"
        ]
    },
    
    "future_opportunity": {
        "title": "⏰ Future Opportunity",
        "conversation": """
        Sales Rep: Hi David, thanks for your interest in our sales automation platform.

        Prospect: Hi. I'm just gathering information for now. We're not ready to make any changes yet.

        Sales Rep: No problem at all. Can you tell me a bit about your current situation and what you're planning for the future?

        Prospect: We're a growing company with 25 salespeople. We're using an old CRM system that's not meeting our needs, but we're focused on other priorities right now.

        Sales Rep: I understand. What are your main priorities for the next 6-12 months?

        Prospect: We're launching a new product line and expanding into new markets. Once that's settled, we'll look at upgrading our sales tools.

        Sales Rep: That makes sense. What specific challenges are you experiencing with your current CRM?

        Prospect: It's slow, doesn't integrate well with our other tools, and the reporting is limited. But we've learned to work around these issues for now.

        Sales Rep: I see. When do you think you'll be ready to evaluate new solutions?

        Prospect: Probably in 6-9 months, once our expansion is complete and we have a better sense of our new sales process.

        Sales Rep: That's a good timeline. Would you be interested in staying in touch? I can send you relevant content and keep you updated on new features.

        Prospect: Sure, that would be fine. Just don't be too pushy about it.

        Sales Rep: Absolutely. I'll add you to our newsletter and reach out occasionally with relevant updates. Is there anything specific you'd like to learn more about?

        Prospect: Maybe some case studies of companies similar to ours. Thanks for understanding our timeline.
        """,
        "expected_score": "Low (20-40)",
        "key_insights": [
            "No immediate urgency",
            "Long timeline (6-9 months)",
            "Clear future need identified",
            "Good for nurture campaign"
        ]
    },
    
    "objection_heavy": {
        "title": "🚫 Objection-Heavy Lead",
        "conversation": """
        Sales Rep: Hi Robert, thanks for taking my call about our sales automation solution.

        Prospect: I'm not really interested. We're doing fine with what we have.

        Sales Rep: I understand. Can you tell me a bit about your current setup?

        Prospect: We use Excel and it works fine for us. I don't see why we need to change.

        Sales Rep: How many salespeople do you have on your team?

        Prospect: 10, but we're not having any problems. Sales are up this year.

        Sales Rep: That's great to hear! What's your process for following up with leads?

        Prospect: We call them when we have time. It's not that complicated.

        Sales Rep: I see. Have you ever missed any opportunities because of follow-up delays?

        Prospect: Maybe, but that's just part of doing business. I'm not convinced that software will solve our problems.

        Sales Rep: What would it take to convince you that a CRM could help your team?

        Prospect: I don't know. We've tried other solutions before and they were just a waste of money. Everyone stopped using them after a few weeks.

        Sales Rep: I understand that concern. What happened with the previous solutions you tried?

        Prospect: They were too complicated, took too long to set up, and my team just went back to their old ways. I'm not interested in going through that again.

        Sales Rep: That's a valid concern. Our platform is designed to be simple and quick to implement. Would you be open to a 30-day free trial to see the difference?

        Prospect: I don't think so. We're busy enough as it is. Maybe call me back in a few months if you're still around.

        Sales Rep: I understand. Thanks for your time today. If you change your mind, feel free to reach out.

        Prospect: Sure. Goodbye.
        """,
        "expected_score": "Very Low (10-25)",
        "key_insights": [
            "Multiple strong objections",
            "Previous negative experiences",
            "Resistance to change",
            "No immediate pain points acknowledged"
        ]
    }
}

# Demo conversation for quick testing
QUICK_TEST_CONVERSATION = """
Sales Rep: Hi there! Thanks for taking the time to speak with me today. I understand you're interested in our sales automation platform.

Prospect: Yes, we're looking for something to help us manage our leads better. We have about 20 salespeople and we're losing deals because we can't track everything properly.

Sales Rep: That's a common challenge. Can you tell me more about your current process?

Prospect: We're using a basic CRM but it's not really helping us close more deals. Our team isn't using it consistently, and we need something that can automate follow-ups.

Sales Rep: I see. What's your timeline for implementing a solution?

Prospect: We need this within the next month. Our Q4 targets are at risk, and I need to show results to my CEO.

Sales Rep: That's definitely achievable. What's your budget range?

Prospect: We're looking to spend around $10,000-$15,000 annually. But I need to see clear ROI and get approval from our CFO.

Sales Rep: Perfect. Our enterprise plan would fit your budget and includes all the automation features you need. Can I send you a proposal with ROI analysis?

Prospect: Yes, that would be great. Can you also schedule a demo for next week? I'll get the team together.

Sales Rep: Absolutely! How about Tuesday at 2 PM?

Prospect: That works. I'm looking forward to seeing how this can help us hit our targets.
"""

# Demo data for different industries
INDUSTRY_DEMO_DATA = {
    "technology": {
        "company_size": "50-200 employees",
        "pain_points": ["Complex sales cycles", "Technical product demos", "Multiple stakeholders"],
        "budget_range": "$15,000-$50,000",
        "timeline": "2-3 months"
    },
    "healthcare": {
        "company_size": "100-500 employees", 
        "pain_points": ["Compliance requirements", "Long sales cycles", "Multiple decision makers"],
        "budget_range": "$20,000-$75,000",
        "timeline": "3-6 months"
    },
    "finance": {
        "company_size": "200-1000 employees",
        "pain_points": ["Regulatory compliance", "Risk management", "Complex approval processes"],
        "budget_range": "$25,000-$100,000", 
        "timeline": "4-8 months"
    },
    "manufacturing": {
        "company_size": "100-500 employees",
        "pain_points": ["Long sales cycles", "Technical specifications", "Multiple departments"],
        "budget_range": "$10,000-$40,000",
        "timeline": "2-4 months"
    }
}

# Demo coaching scenarios
COACHING_SCENARIOS = {
    "price_objection": {
        "title": "Handling Price Objection",
        "scenario": "Prospect says: 'Your solution is too expensive. We can get something similar for half the price.'",
        "best_practices": [
            "Acknowledge the concern about budget",
            "Focus on value and ROI, not just price",
            "Ask about the total cost of ownership",
            "Provide case studies with ROI examples"
        ],
        "sample_script": "I understand budget is important. Let me show you how our solution delivers ROI within 6 months. What's the cost of losing deals due to poor follow-up?"
    },
    "timing_objection": {
        "title": "Handling Timing Objection", 
        "scenario": "Prospect says: 'We're not ready to make a decision right now. Call us back in 6 months.'",
        "best_practices": [
            "Understand what needs to happen first",
            "Create urgency with opportunity cost",
            "Offer a pilot program",
            "Set specific follow-up timeline"
        ],
        "sample_script": "When you say timing, what specifically needs to happen before you're ready to move forward? What's the cost of waiting 6 months?"
    },
    "competitor_comparison": {
        "title": "Handling Competitor Comparison",
        "scenario": "Prospect says: 'We're also looking at Salesforce. Why should we choose you instead?'",
        "best_practices": [
            "Acknowledge the competitor's strengths",
            "Focus on your unique advantages",
            "Ask about their specific needs",
            "Provide comparison data"
        ],
        "sample_script": "Salesforce is a great platform. What specific features are most important to you? Let me show you how we excel in those areas."
    }
}

def get_demo_conversation(key):
    """Get a specific demo conversation"""
    return DEMO_CONVERSATIONS.get(key, {})

def get_all_demo_conversations():
    """Get all demo conversations"""
    return DEMO_CONVERSATIONS

def get_quick_test_conversation():
    """Get the quick test conversation"""
    return QUICK_TEST_CONVERSATION

def get_industry_demo_data():
    """Get industry-specific demo data"""
    return INDUSTRY_DEMO_DATA

def get_coaching_scenarios():
    """Get coaching scenarios"""
    return COACHING_SCENARIOS

if __name__ == "__main__":
    print("Demo Data for LLM Lead Generation Coaching Tool")
    print("=" * 50)
    print(f"Available conversations: {len(DEMO_CONVERSATIONS)}")
    print(f"Available industries: {len(INDUSTRY_DEMO_DATA)}")
    print(f"Available coaching scenarios: {len(COACHING_SCENARIOS)}")
    
    print("\nQuick test conversation preview:")
    print(QUICK_TEST_CONVERSATION[:200] + "...") 