import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Together AI Configuration
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
TOGETHER_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

# Model parameters
DEFAULT_MODEL_PARAMS = {
    'temperature': 0.7,
    'max_tokens': 1024,
    'top_p': 0.9,
    'top_k': 50
}

# Available models for different tasks (using actual model names)
MODELS = {
    'conversation_analysis': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
    'lead_scoring': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
    'coaching': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
    'insights': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'
}

# Alternative models if the above are not available
ALTERNATIVE_MODELS = {
    'conversation_analysis': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
    'lead_scoring': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
    'coaching': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
    'insights': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'
} 