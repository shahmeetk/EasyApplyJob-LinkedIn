from config.secrets import *
from modules.helpers import print_lg
from typing import Dict, List, Any, Union, Literal

# Import AI provider modules
try:
    from modules.ai.openaiConnections import *
except ImportError:
    print_lg("OpenAI module not available")

try:
    from modules.ai.ollamaConnections import *
except ImportError:
    print_lg("Ollama module not available")

# Global client for OpenAI
openai_client = None

def initialize_ai():
    """
    Initialize the AI system based on the configured provider.
    Returns True if initialization was successful, False otherwise.
    """
    global openai_client

    # Check if AI is enabled in configuration
    if not globals().get('use_AI', False):
        print_lg("AI is disabled in configuration")
        return False

    try:
        # Get AI provider from globals
        provider = globals().get('ai_provider', 'unknown').lower()

        if provider == "ollama":
            # Check if Ollama is running
            if not ollama_is_running():
                print_lg("Ollama is not running. Please start Ollama and try again.")
                if not globals().get('use_AI_if_ollama_not_running', False):
                    print_lg("Disabling AI functionality as Ollama is not running")
                    return False
                else:
                    print_lg("Continuing without AI functionality as Ollama is not running")
                    return False

            # Get Ollama model from globals
            ollama_model_name = globals().get('ollama_model', 'gemma3:4b')

            # Check if the configured model exists
            if not ollama_model_exists(ollama_model_name):
                print_lg(f"Model '{ollama_model_name}' not found in Ollama. Please pull the model or choose another one.")
                if not globals().get('use_AI_if_ollama_not_running', False):
                    print_lg("Disabling AI functionality as the model is not available")
                    return False
                else:
                    print_lg("Continuing without AI functionality as the model is not available")
                    return False

            print_lg(f"Successfully initialized Ollama with model: {ollama_model_name}")
            return True

        elif provider == "openai":
            # Initialize OpenAI client
            openai_client = ai_create_openai_client()
            if openai_client:
                print_lg("Successfully initialized OpenAI client")
                return True
            else:
                print_lg("Failed to initialize OpenAI client")
                return False

        else:
            print_lg(f"Unknown AI provider: {provider}. Please use 'ollama' or 'openai'.")
            return False

    except Exception as e:
        print_lg(f"Error initializing AI: {str(e)}")
        return False

def extract_skills(job_description: str) -> Dict:
    """
    Extract skills from a job description using the configured AI provider.
    """
    # Check if AI is enabled in configuration
    if not globals().get('use_AI', False):
        print_lg("AI is disabled, cannot extract skills")
        return {"error": "AI is disabled"}

    try:
        # Get the AI provider from global configuration
        provider = globals().get('ai_provider', 'unknown').lower()

        if provider == "ollama":
            print_lg("Using Ollama to extract skills")
            return ollama_extract_skills(job_description)
        elif provider == "openai" and openai_client:
            print_lg("Using OpenAI to extract skills")
            return ai_extract_skills(openai_client, job_description)
        else:
            print_lg(f"No valid AI provider configured: {provider}")
            return {"error": f"No valid AI provider configured: {provider}"}
    except Exception as e:
        print_lg(f"Error extracting skills: {str(e)}")
        return {"error": f"Error extracting skills: {str(e)}"}

def answer_question(
    question: str,
    options: List[str] = None,
    question_type: Literal['text', 'textarea', 'single_select', 'multiple_select'] = 'text',
    job_description: str = None,
    about_company: str = None,
    user_information_all: str = None
) -> str:
    """
    Generate an answer to a question using the configured AI provider.
    """
    # Check if AI is enabled in configuration
    if not globals().get('use_AI', False):
        print_lg("AI is disabled, cannot answer question")
        return "AI is disabled"

    try:
        # Get the AI provider from global configuration
        provider = globals().get('ai_provider', 'unknown').lower()

        if provider == "ollama":
            print_lg(f"Using Ollama to answer question: {question}")
            return ollama_answer_question(
                question,
                options,
                question_type,
                job_description,
                about_company,
                user_information_all
            )
        elif provider == "openai" and openai_client:
            print_lg(f"Using OpenAI to answer question: {question}")
            return ai_answer_question(
                openai_client,
                question,
                options,
                question_type,
                job_description,
                about_company,
                user_information_all
            )
        else:
            print_lg(f"No valid AI provider configured: {provider}")
            return f"No valid AI provider configured: {provider}"
    except Exception as e:
        print_lg(f"Error answering question: {str(e)}")
        return f"Error answering question: {str(e)}"

def cleanup_ai():
    """
    Clean up AI resources when the application is closing.
    """
    global openai_client

    # Get AI provider from globals
    provider = globals().get('ai_provider', 'unknown').lower()

    if provider == "openai" and openai_client:
        try:
            print_lg("Cleaning up OpenAI resources...")
            ai_close_openai_client(openai_client)
            openai_client = None
            print_lg("OpenAI resources cleaned up successfully")
        except Exception as e:
            print_lg(f"Error closing OpenAI client: {str(e)}")
    elif provider == "ollama":
        print_lg("No cleanup needed for Ollama")
