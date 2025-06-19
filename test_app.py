#!/usr/bin/env python3
"""
Test script for LLM Lead Generation Coaching Tool
"""

import sys
import os
from textblob import TextBlob

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test basic imports"""
    print("🧪 Testing basic imports...")
    try:
        import streamlit as st
        import pandas as pd
        import numpy as np
        import plotly.express as px
        from textblob import TextBlob
        import json
        print("✅ All basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    try:
        from config import TOGETHER_API_KEY, DEFAULT_MODEL_PARAMS, MODELS
        print(f"✅ Config loaded successfully")
        print(f"   API Key configured: {'Yes' if TOGETHER_API_KEY else 'No'}")
        print(f"   Default model params: {DEFAULT_MODEL_PARAMS}")
        print(f"   Available models: {list(MODELS.keys())}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_llm_service():
    """Test LLM service"""
    print("\n🧪 Testing LLM service...")
    try:
        from llm_service import LLMService
        print("✅ LLM service imported successfully")
        
        # Test fallback methods
        service = LLMService()
        print("✅ LLM service initialized")
        
        # Test fallback analysis
        test_conversation = "Hello, I'm interested in your product. What are the pricing options?"
        fallback_analysis = service._fallback_analysis(test_conversation)
        print(f"✅ Fallback analysis works: {len(fallback_analysis)} fields")
        
        # Test fallback scoring
        fallback_score = service._fallback_scoring(fallback_analysis)
        print(f"✅ Fallback scoring works: score = {fallback_score['overall_score']}")
        
        return True
    except Exception as e:
        print(f"❌ LLM service error: {e}")
        return False

def test_lead_analyzer():
    """Test original lead analyzer"""
    print("\n🧪 Testing original lead analyzer...")
    try:
        from leadscore import LeadAnalyzer
        analyzer = LeadAnalyzer()
        print("✅ Lead analyzer initialized")
        
        # Test conversation analysis
        test_conversation = "I'm looking for a solution to improve our sales process. What do you offer?"
        analysis = analyzer.analyze_conversation(test_conversation)
        print(f"✅ Analysis completed: score = {analysis['lead_score']:.1f}")
        print(f"   Sentiment: {analysis['sentiment'].polarity:.2f}")
        print(f"   Engagement: {analysis['engagement_level']}")
        
        return True
    except Exception as e:
        print(f"❌ Lead analyzer error: {e}")
        return False

def test_sample_data():
    """Test sample data generation"""
    print("\n🧪 Testing sample data generation...")
    try:
        from leadscore import create_sample_data
        df = create_sample_data()
        print(f"✅ Sample data created: {len(df)} records")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Lead scores range: {df['Lead_Score'].min()} - {df['Lead_Score'].max()}")
        
        return True
    except Exception as e:
        print(f"❌ Sample data error: {e}")
        return False

def test_coaching_recommendations():
    """Test coaching recommendations"""
    print("\n🧪 Testing coaching recommendations...")
    try:
        from leadscore import generate_coaching_recommendations
        
        # Create test analysis
        test_analysis = {
            'lead_score': 75,
            'sentiment': TextBlob("I'm very interested in your solution").sentiment,
            'keyword_counts': {
                'interest': 2,
                'buying_signals': 1,
                'objection': 0
            }
        }
        
        recommendations = generate_coaching_recommendations(test_analysis)
        print(f"✅ Coaching recommendations generated: {len(recommendations)} items")
        for rec in recommendations:
            print(f"   - {rec['action']} ({rec['priority']} priority)")
        
        return True
    except Exception as e:
        print(f"❌ Coaching recommendations error: {e}")
        return False

def test_llm_fallback():
    """Test LLM fallback functionality"""
    print("\n🧪 Testing LLM fallback functionality...")
    try:
        from llm_service import LLMService
        
        # Create service without API key (should use fallbacks)
        original_key = os.environ.get('TOGETHER_API_KEY', '')
        if 'TOGETHER_API_KEY' in os.environ:
            del os.environ['TOGETHER_API_KEY']
        
        # This should work with fallbacks
        service = LLMService()
        
        test_conversation = "I need a CRM solution for my small business."
        
        # Test fallback analysis
        analysis = service.analyze_conversation_llm(test_conversation)
        print(f"✅ Fallback analysis: {analysis['lead_quality']} quality lead")
        
        # Test fallback scoring
        score = service.generate_lead_score_llm(analysis)
        print(f"✅ Fallback scoring: {score['overall_score']}/100")
        
        # Test fallback coaching
        coaching = service.generate_coaching_recommendations_llm(analysis, score)
        print(f"✅ Fallback coaching: {len(coaching)} recommendations")
        
        # Restore API key
        if original_key:
            os.environ['TOGETHER_API_KEY'] = original_key
        
        return True
    except Exception as e:
        print(f"❌ LLM fallback error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 LLM Lead Generation Coaching Tool - Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_imports,
        test_config,
        test_llm_service,
        test_lead_analyzer,
        test_sample_data,
        test_coaching_recommendations,
        test_llm_fallback
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n📋 Next steps:")
        print("1. Set your Together AI API key in .env file")
        print("2. Run: streamlit run leadscore.py")
        print("3. Open your browser to the provided URL")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 