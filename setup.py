#!/usr/bin/env python3
"""
Setup script for LLM Lead Generation Coaching Tool
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with user input"""
    print("🔧 Setting up Together AI API Key...")
    
    api_key = input("Enter your Together AI API key: ").strip()
    if not api_key:
        print("❌ API key is required!")
        return False
    
    model = input("Enter model name (default: llama-3.1-8b-instant): ").strip()
    if not model:
        model = "llama-3.1-8b-instant"
    
    env_content = f"""# Together AI Configuration
TOGETHER_API_KEY={api_key}
TOGETHER_MODEL={model}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'textblob',
        'together',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📥 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def main():
    """Main setup function"""
    print("🚀 LLM Lead Generation Coaching Tool Setup")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️ .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n📥 Please install missing dependencies and run setup again.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: streamlit run leadscore.py")
    print("2. Open your browser to the provided URL")
    print("3. Start using the AI-powered lead generation tool!")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 