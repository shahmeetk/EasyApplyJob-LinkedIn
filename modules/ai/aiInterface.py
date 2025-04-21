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
    
    if not use_AI:
        print_lg("AI is disabled in configuration")
        return False
        
    try:
        if ai_provider.lower() == "ollama":
            # Check if Ollama is running
            if not ollama_is_running():
                print_lg("Ollama is not running. Please start Ollama and try again.")
                if not use_AI_if_ollama_not_running:
                    print_lg("Disabling AI functionality as Ollama is not running")
                    return False
                else:
                    print_lg("Continuing without AI functionality as Ollama is not running")
                    return False
                    
            # Check if the configured model exists
            if not ollama_model_exists(ollama_model):
                print_lg(f"Model '{ollama_model}' not found in Ollama. Please pull the model or choose another one.")
                if not use_AI_if_ollama_not_running:
                    print_lg("Disabling AI functionality as the model is not available")
                    return False
                else:
                    print_lg("Continuing without AI functionality as the model is not available")
                    return False
                    
            print_lg(f"Successfully initialized Ollama with model: {ollama_model}")
            return True
            
        elif ai_provider.lower() == "openai":
            # Initialize OpenAI client
            openai_client = ai_create_openai_client()
            if openai_client:
                print_lg("Successfully initialized OpenAI client")
                return True
            else:
                print_lg("Failed to initialize OpenAI client")
                return False
                
        else:
            print_lg(f"Unknown AI provider: {ai_provider}. Please use 'ollama' or 'openai'.")
            return False
            
    except Exception as e:
        print_lg(f"Error initializing AI: {str(e)}")
        return False

def extract_skills(job_description: str) -> Dict:
    """
    Extract skills from a job description using the configured AI provider.
    """
    if not use_AI:
        return {"error": "AI is disabled"}
        
    try:
        if ai_provider.lower() == "ollama":
            return ollama_extract_skills(job_description)
        elif ai_provider.lower() == "openai" and openai_client:
            return ai_extract_skills(openai_client, job_description)
        else:
            return {"error": "No valid AI provider configured"}
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
    if not use_AI:
        return "AI is disabled"
        
    try:
        if ai_provider.lower() == "ollama":
            return ollama_answer_question(
                question, 
                options, 
                question_type,
                job_description, 
                about_company, 
                user_information_all
            )
        elif ai_provider.lower() == "openai" and openai_client:
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
            return "No valid AI provider configured"
    except Exception as e:
        print_lg(f"Error answering question: {str(e)}")
        return f"Error answering question: {str(e)}"

def cleanup_ai():
    """
    Clean up AI resources when the application is closing.
    """
    global openai_client
    
    if ai_provider.lower() == "openai" and openai_client:
        try:
            ai_close_openai_client(openai_client)
            openai_client = None
        except Exception as e:
            print_lg(f"Error closing OpenAI client: {str(e)}")
