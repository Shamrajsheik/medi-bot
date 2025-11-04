import os
from dotenv import load_dotenv

import google.generativeai as genai

def test_gemini_api():
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment variable
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            raise ValueError("API key not found in environment variables")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # List available models
        print("Available Models:")
        for model in genai.list_models():
            if 'gemini' in model.name:
                print(f"Model Name: {model.name}")
                print(f"Display Name: {model.display_name}")
                print(f"Description: {model.description}")
                print(f"Generation Methods: {model.supported_generation_methods}")
                print("-" * 50)
                
        return True
        
    except Exception as e:
        print(f"Error testing Gemini API: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api()