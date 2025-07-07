#!/usr/bin/env python3
"""
Environment setup script for AdaTAMP
This script helps configure the necessary environment variables and paths.
"""

import os
import sys

def setup_environment():
    """Interactive setup for AdaTAMP environment"""
    print("🔧 AdaTAMP Environment Setup")
    print("=" * 40)
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print()
    else:
        print("✅ OPENAI_API_KEY is configured")
    
    # Check VirtualHome path
    vh_path = input("Enter the path to your VirtualHome executable (e.g., virtualhome/macos_exec.2.2.4.app): ").strip()
    
    if vh_path:
        # Update the evaluate.py file
        try:
            with open('src/evaluate.py', 'r') as f:
                content = f.read()
            
            # Replace the YOUR_FILE_NAME line
            import re
            content = re.sub(
                r'YOUR_FILE_NAME = "[^"]*"',
                f'YOUR_FILE_NAME = "{vh_path}"',
                content
            )
            
            with open('src/evaluate.py', 'w') as f:
                f.write(content)
            
            print(f"✅ Updated VirtualHome path to: {vh_path}")
        except Exception as e:
            print(f"❌ Error updating path: {e}")
    
    print("\n📋 Next steps:")
    print("1. Make sure VirtualHome is properly installed")
    print("2. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
    print("3. Run: python src/evaluate.py")
    print("\n🔒 Security reminder: Never commit API keys or personal paths to version control!")

if __name__ == "__main__":
    setup_environment() 