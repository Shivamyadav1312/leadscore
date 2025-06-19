import together
import json
import streamlit as st
from typing import Dict, List, Any, Optional
from config import TOGETHER_API_KEY, DEFAULT_MODEL_PARAMS, MODELS

class LLMService:
    def __init__(self):
        self.api_key_available = bool(TOGETHER_API_KEY)
        
        if not self.api_key_available:
            # Don't initialize Together client if no API key
            self.client = None
        else:
            try:
                together.api_key = TOGETHER_API_KEY
                # Together AI now uses Complete.create() method
                self.client = together.Complete
            except Exception as e:
                self._show_warning(f"Failed to initialize Together AI client: {str(e)}")
                self.client = None
                self.api_key_available = False
    
    def _show_warning(self, message: str):
        """Safely show warning in Streamlit or print to console"""
        try:
            if hasattr(st, 'warning'):
                st.warning(message)
            else:
                print(f"Warning: {message}")
        except:
            print(f"Warning: {message}")
    
    def analyze_conversation_llm(self, conversation: str, timing_context: dict = None) -> Dict[str, Any]:
        """Use LLM to analyze sales conversation with advanced insights and timing context"""
        
        if not self.api_key_available or not self.client:
            return self._fallback_analysis(conversation, timing_context)
        
        # Build timing context string
        timing_info = ""
        if timing_context:
            timing_info = f"""
            CONVERSATION TIMING:
            - Date: {timing_context.get('date', 'Not specified')}
            - Time: {timing_context.get('time', 'Not specified')}
            - Duration: {timing_context.get('duration', 'Not specified')}
            - Day of Week: {timing_context.get('day_of_week', 'Not specified')}
            - Time Since: {timing_context.get('time_since', 'Not specified')}
            
            """
        
        prompt = f"""
        Analyze this sales conversation and provide detailed insights:

        {timing_info}
        CONVERSATION:
        {conversation}

        Please provide a JSON response with the following structure:
        {{
            "sentiment_score": float (-1 to 1),
            "engagement_level": "Low/Medium/High",
            "buying_intent": "Low/Medium/High",
            "key_topics": ["topic1", "topic2", "topic3"],
            "pain_points": ["pain1", "pain2"],
            "objections": ["objection1", "objection2"],
            "buying_signals": ["signal1", "signal2"],
            "decision_maker_indicators": ["indicator1", "indicator2"],
            "urgency_level": "Low/Medium/High",
            "budget_mentions": "Yes/No",
            "timeline_mentions": "Yes/No",
            "competitor_mentions": "Yes/No",
            "next_steps_suggested": ["step1", "step2"],
            "risk_factors": ["risk1", "risk2"],
            "opportunity_size": "Small/Medium/Large",
            "lead_quality": "Poor/Fair/Good/Excellent",
            "timing_insights": ["timing_insight1", "timing_insight2"],
            "optimal_follow_up_time": "Immediate/Within 24h/Within 48h/This week/Next week"
        }}

        Focus on sales-specific insights and actionable recommendations. Consider the timing context when available.
        """
        
        try:
            # Use the correct API method
            response = together.Complete.create(
                model=MODELS['conversation_analysis'],
                prompt=prompt,
                max_tokens=DEFAULT_MODEL_PARAMS['max_tokens'],
                temperature=DEFAULT_MODEL_PARAMS['temperature'],
                top_p=DEFAULT_MODEL_PARAMS['top_p'],
                top_k=DEFAULT_MODEL_PARAMS['top_k']
            )
            
            # Extract text from response - fixed structure
            result_text = response['choices'][0]['text']
            # Clean the response and extract JSON - improved extraction
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = result_text[json_start:json_end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Try to find valid JSON by looking for the last complete JSON object
                    import re
                    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                    matches = re.findall(json_pattern, result_text)
                    if matches:
                        try:
                            return json.loads(matches[-1])  # Use the last complete JSON object
                        except json.JSONDecodeError:
                            pass
            return self._fallback_analysis(conversation, timing_context)
                
        except Exception as e:
            self._show_warning(f"LLM analysis failed: {str(e)}. Using fallback analysis.")
            return self._fallback_analysis(conversation, timing_context)
    
    def generate_lead_score_llm(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Use LLM to generate sophisticated lead scoring"""
        
        if not self.api_key_available or not self.client:
            return self._fallback_scoring(analysis)
        
        analysis_str = json.dumps(analysis, indent=2)
        
        prompt = f"""
        Based on this conversation analysis, calculate a comprehensive lead score:

        ANALYSIS:
        {analysis_str}

        Please provide a JSON response with:
        {{
            "overall_score": int (0-100),
            "score_breakdown": {{
                "buying_intent": int (0-25),
                "decision_power": int (0-20),
                "urgency": int (0-15),
                "budget_availability": int (0-15),
                "fit_score": int (0-15),
                "engagement": int (0-10)
            }},
            "score_explanation": "Detailed explanation of the score",
            "priority_level": "Low/Medium/High/Critical",
            "recommended_action": "Specific next action to take",
            "timeline": "Immediate/This Week/This Month/Long-term",
            "confidence_level": "Low/Medium/High"
        }}
        """
        
        try:
            response = together.Complete.create(
                model=MODELS['lead_scoring'],
                prompt=prompt,
                max_tokens=DEFAULT_MODEL_PARAMS['max_tokens'],
                temperature=DEFAULT_MODEL_PARAMS['temperature'],
                top_p=DEFAULT_MODEL_PARAMS['top_p'],
                top_k=DEFAULT_MODEL_PARAMS['top_k']
            )
            
            result_text = response['choices'][0]['text']
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = result_text[json_start:json_end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Try to find valid JSON by looking for the last complete JSON object
                    import re
                    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                    matches = re.findall(json_pattern, result_text)
                    if matches:
                        try:
                            return json.loads(matches[-1])  # Use the last complete JSON object
                        except json.JSONDecodeError:
                            pass
            return self._fallback_scoring(analysis)
                
        except Exception as e:
            self._show_warning(f"LLM scoring failed: {str(e)}. Using fallback scoring.")
            return self._fallback_scoring(analysis)
    
    def generate_coaching_recommendations_llm(self, analysis: Dict[str, Any], score_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use LLM to generate personalized coaching recommendations"""
        
        if not self.api_key_available or not self.client:
            return self._fallback_coaching(analysis, score_data)
        
        analysis_str = json.dumps(analysis, indent=2)
        score_str = json.dumps(score_data, indent=2)
        
        prompt = f"""
        Generate personalized coaching recommendations for this sales situation:

        CONVERSATION ANALYSIS:
        {analysis_str}

        LEAD SCORE DATA:
        {score_str}

        Provide a JSON array of coaching recommendations:
        [
            {{
                "priority": "High/Medium/Low",
                "category": "Objection Handling/Discovery/Closing/Follow-up",
                "action": "Specific action to take",
                "reason": "Why this action is recommended",
                "script": "Sample script or approach",
                "timeline": "When to implement",
                "expected_outcome": "What this should achieve"
            }}
        ]

        Focus on actionable, specific advice tailored to this situation.
        """
        
        try:
            response = together.Complete.create(
                model=MODELS['coaching'],
                prompt=prompt,
                max_tokens=DEFAULT_MODEL_PARAMS['max_tokens'],
                temperature=DEFAULT_MODEL_PARAMS['temperature'],
                top_p=DEFAULT_MODEL_PARAMS['top_p'],
                top_k=DEFAULT_MODEL_PARAMS['top_k']
            )
            
            result_text = response['choices'][0]['text']
            json_start = result_text.find('[')
            json_end = result_text.rfind(']') + 1
            if json_start != -1 and json_end != 0:
                json_str = result_text[json_start:json_end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Try to find valid JSON array by looking for the last complete array
                    import re
                    array_pattern = r'\[[^\[\]]*(?:\{[^{}]*\}[^\[\]]*)*\]'
                    matches = re.findall(array_pattern, result_text)
                    if matches:
                        try:
                            return json.loads(matches[-1])  # Use the last complete array
                        except json.JSONDecodeError:
                            pass
            return self._fallback_coaching(analysis, score_data)
                
        except Exception as e:
            self._show_warning(f"LLM coaching failed: {str(e)}. Using fallback coaching.")
            return self._fallback_coaching(analysis, score_data)
    
    def generate_insights_llm(self, conversation: str, analysis: Dict[str, Any]) -> List[str]:
        """Use LLM to generate advanced insights"""
        
        if not self.api_key_available or not self.client:
            return self._fallback_insights(analysis)
        
        analysis_str = json.dumps(analysis, indent=2)
        
        prompt = f"""
        Generate advanced insights from this sales conversation:

        CONVERSATION:
        {conversation}

        ANALYSIS:
        {analysis_str}

        Provide a JSON array of insights:
        [
            "Insight 1 with emoji",
            "Insight 2 with emoji",
            "Insight 3 with emoji"
        ]

        Focus on:
        - Hidden opportunities
        - Potential risks
        - Strategic recommendations
        - Behavioral patterns
        - Competitive advantages
        """
        
        try:
            response = together.Complete.create(
                model=MODELS['insights'],
                prompt=prompt,
                max_tokens=DEFAULT_MODEL_PARAMS['max_tokens'],
                temperature=DEFAULT_MODEL_PARAMS['temperature'],
                top_p=DEFAULT_MODEL_PARAMS['top_p'],
                top_k=DEFAULT_MODEL_PARAMS['top_k']
            )
            
            result_text = response['choices'][0]['text']
            json_start = result_text.find('[')
            json_end = result_text.rfind(']') + 1
            if json_start != -1 and json_end != 0:
                json_str = result_text[json_start:json_end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Try to find valid JSON array by looking for the last complete array
                    import re
                    array_pattern = r'\[[^\[\]]*(?:\{[^{}]*\}[^\[\]]*)*\]'
                    matches = re.findall(array_pattern, result_text)
                    if matches:
                        try:
                            return json.loads(matches[-1])  # Use the last complete array
                        except json.JSONDecodeError:
                            pass
            return self._fallback_insights(analysis)
                
        except Exception as e:
            self._show_warning(f"LLM insights failed: {str(e)}. Using fallback insights.")
            return self._fallback_insights(analysis)
    
    def generate_follow_up_email_llm(self, conversation: str, analysis: Dict[str, Any]) -> str:
        """Use LLM to generate personalized follow-up emails"""
        
        if not self.api_key_available or not self.client:
            return self._fallback_email(analysis)
        
        analysis_str = json.dumps(analysis, indent=2)
        
        prompt = f"""
        Generate a personalized follow-up email based on this sales conversation:

        CONVERSATION:
        {conversation}

        ANALYSIS:
        {analysis_str}

        Create a professional, personalized follow-up email that:
        - References specific points from the conversation
        - Addresses any concerns or objections
        - Provides value and next steps
        - Is appropriate for the lead's stage and interest level

        Return only the email content, no JSON formatting.
        """
        
        try:
            response = together.Complete.create(
                model=MODELS['coaching'],
                prompt=prompt,
                max_tokens=DEFAULT_MODEL_PARAMS['max_tokens'],
                temperature=DEFAULT_MODEL_PARAMS['temperature'],
                top_p=DEFAULT_MODEL_PARAMS['top_p'],
                top_k=DEFAULT_MODEL_PARAMS['top_k']
            )
            
            return response['choices'][0]['text'].strip()
                
        except Exception as e:
            self._show_warning(f"LLM email generation failed: {str(e)}. Using fallback email.")
            return self._fallback_email(analysis)
    
    def _fallback_analysis(self, conversation: str, timing_context: dict = None) -> Dict[str, Any]:
        """Fallback analysis when LLM fails"""
        base_analysis = {
            "sentiment_score": 0.0,
            "engagement_level": "Medium",
            "buying_intent": "Medium",
            "key_topics": ["general discussion"],
            "pain_points": [],
            "objections": [],
            "buying_signals": [],
            "decision_maker_indicators": [],
            "urgency_level": "Low",
            "budget_mentions": "No",
            "timeline_mentions": "No",
            "competitor_mentions": "No",
            "next_steps_suggested": ["Schedule follow-up"],
            "risk_factors": [],
            "opportunity_size": "Medium",
            "lead_quality": "Fair",
            "timing_insights": [],
            "optimal_follow_up_time": "Within 48h"
        }
        
        # Add timing insights if available
        if timing_context:
            duration = timing_context.get('duration', '')
            day_of_week = timing_context.get('day_of_week', '')
            time_since = timing_context.get('time_since', '')
            
            timing_insights = []
            if duration:
                if 'hour' in duration.lower():
                    timing_insights.append(f"📊 Extended conversation ({duration}) indicates high engagement")
                else:
                    timing_insights.append(f"📊 Brief conversation ({duration}) - may need more discovery")
            
            if day_of_week:
                if day_of_week in ['Monday', 'Tuesday', 'Wednesday']:
                    timing_insights.append("📅 Early week conversation - good for follow-up planning")
                elif day_of_week in ['Thursday', 'Friday']:
                    timing_insights.append("📅 End of week conversation - consider Monday follow-up")
                else:
                    timing_insights.append("📅 Weekend conversation - unusual timing, may indicate urgency")
            
            if time_since:
                if 'hours' in time_since and int(time_since.split()[0]) < 24:
                    timing_insights.append("⏰ Recent conversation - optimal time for immediate follow-up")
                    base_analysis["optimal_follow_up_time"] = "Immediate"
                elif 'days' in time_since and int(time_since.split()[0]) < 3:
                    timing_insights.append("⏰ Older conversation - may need re-engagement strategy")
                    base_analysis["optimal_follow_up_time"] = "This week"
            
            base_analysis["timing_insights"] = timing_insights
        
        return base_analysis
    
    def _fallback_scoring(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback scoring when LLM fails"""
        return {
            "overall_score": 50,
            "score_breakdown": {
                "buying_intent": 12,
                "decision_power": 10,
                "urgency": 7,
                "budget_availability": 7,
                "fit_score": 7,
                "engagement": 7
            },
            "score_explanation": "Standard scoring applied",
            "priority_level": "Medium",
            "recommended_action": "Follow up within 48 hours",
            "timeline": "This Week",
            "confidence_level": "Medium"
        }
    
    def _fallback_coaching(self, analysis: Dict[str, Any], score_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback coaching when LLM fails"""
        return [
            {
                "priority": "Medium",
                "category": "Follow-up",
                "action": "Schedule follow-up call",
                "reason": "Standard follow-up recommended",
                "script": "Thank you for your time. Let's schedule a follow-up...",
                "timeline": "Within 48 hours",
                "expected_outcome": "Continued engagement"
            }
        ]
    
    def _fallback_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Fallback insights when LLM fails"""
        return [
            "📊 Standard analysis completed",
            "💡 Consider scheduling follow-up",
            "🎯 Monitor engagement levels"
        ]
    
    def _fallback_email(self, analysis: Dict[str, Any]) -> str:
        """Fallback email when LLM fails"""
        return """
        Dear [Prospect Name],

        Thank you for taking the time to speak with me today. I enjoyed our conversation and learning more about your business needs.

        As discussed, I'll follow up with you within the next few days to continue our conversation and explore how we can help address your challenges.

        Best regards,
        [Your Name]
        """ 