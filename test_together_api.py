#!/usr/bin/env python3
"""
Test script for Together AI API
"""

import together
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_together_api():
    """Test Together AI API directly"""
    print("🔄 Testing API call...")
    try:
        response = together.Complete.create(
            prompt="Hello, how are you?",
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",  # Updated model name
            max_tokens=50,
            temperature=0.7
        )
        print("✅ API call successful!")
        return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_llm_service():
    """Test our LLM service with the updated API"""
    print("\n🧪 Testing LLM Service...")
    
    try:
        from llm_service import LLMService
        
        service = LLMService()
        print(f"✅ LLM Service initialized. API available: {service.api_key_available}")
        
        if service.api_key_available:
            # Test fallback analysis
            test_conversation = "Hello, I'm interested in your product. What are the pricing options?"
            analysis = service.analyze_conversation_llm(test_conversation)
            print(f"✅ Analysis test completed. Lead quality: {analysis['lead_quality']}")
            
            # Test fallback scoring
            score = service.generate_lead_score_llm(analysis)
            print(f"✅ Scoring test completed. Score: {score['overall_score']}")
            
            # Test fallback coaching
            coaching = service.generate_coaching_recommendations_llm(analysis, score)
            print(f"✅ Coaching test completed. Recommendations: {len(coaching)}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM Service test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Together AI API Test Suite")
    print("=" * 40)
    
    # Test basic API
    api_works = test_together_api()
    
    # Test our service
    service_works = test_llm_service()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"   API Test: {'✅ PASS' if api_works else '❌ FAIL'}")
    print(f"   Service Test: {'✅ PASS' if service_works else '❌ FAIL'}")
    
    if api_works and service_works:
        print("\n🎉 All tests passed! The API is working correctly.")
        print("You can now use the full AI features in your application.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        print("The application will still work with fallback functionality.")

if __name__ == "__main__":
    main() 