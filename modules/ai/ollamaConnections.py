from config.secrets import *
from config.settings import showAiErrorAlerts
from config.personals import ethnicity, gender, disability_status, veteran_status
from config.questions import *
from config.search import security_clearance, did_masters

from modules.helpers import print_lg, critical_error_log, convert_to_json
from modules.ai.prompts import *

from pyautogui import confirm
import requests
import json
from typing import Iterator, Literal, Dict, List, Any, Union

# Error message for Ollama connection issues
ollama_check_instructions = """
1. Make sure Ollama is installed and running on your machine.
2. Check if the Ollama API is accessible at the configured URL (default: http://localhost:11434).
3. Verify that the model you're trying to use is available in Ollama.

To install Ollama, visit: https://ollama.com/download
To start Ollama, run the Ollama application or use the command line.
To check available models, run: 'ollama list' in your terminal.

Open `secrets.py` in the `/config` folder to configure your Ollama settings.

ERROR:
"""

# Function to show an Ollama error alert
def ollama_error_alert(message: str, error: Exception, title: str = "Ollama Connection Error") -> None:
    """
    Function to show an Ollama error alert and log it.
    """
    global showAiErrorAlerts
    if showAiErrorAlerts:
        if "Pause AI error alerts" == confirm(f"{message}\n{ollama_check_instructions}\n{str(error)}", title, ["Pause AI error alerts", "Okay Continue"]):
            showAiErrorAlerts = False
    critical_error_log(message, error)

# Function to check if Ollama is running
def ollama_is_running() -> bool:
    """
    Function to check if Ollama is running.
    Returns True if Ollama is running, False otherwise.
    """
    try:
        response = requests.get(f"{ollama_api_url}/api/tags")
        return response.status_code == 200
    except Exception:
        return False

# Function to get list of models available in Ollama
def ollama_get_models_list() -> List[Dict[str, Any]]:
    """
    Function to get list of models available in Ollama.
    Returns a list of model information dictionaries.
    """
    try:
        print_lg("Getting Ollama models list...")
        response = requests.get(f"{ollama_api_url}/api/tags")
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            print_lg("Available Ollama models:")
            print_lg(models, pretty=True)
            return models
        else:
            error_msg = f"Failed to get Ollama models. Status code: {response.status_code}"
            print_lg(error_msg)
            return [{"error": error_msg}]
    except Exception as e:
        error_msg = f"Error occurred while getting Ollama models list: {str(e)}"
        critical_error_log(error_msg, e)
        return [{"error": error_msg}]

# Function to check if a model exists in Ollama
def ollama_model_exists(model_name: str) -> bool:
    """
    Function to check if a model exists in Ollama.
    Returns True if the model exists, False otherwise.
    """
    try:
        models = ollama_get_models_list()
        if any(isinstance(model, dict) and model.get("error") for model in models):
            return False
            
        return any(model.get("name") == model_name for model in models)
    except Exception:
        return False

# Function to generate completions using Ollama
def ollama_completion(
    messages: List[Dict[str, str]], 
    model: str = ollama_model,
    temperature: float = 0.7,
    stream: bool = stream_output,
    response_format: Dict = None
) -> Union[str, Dict]:
    """
    Function to generate completions using Ollama.
    
    Parameters:
    - messages: List of message dictionaries with 'role' and 'content' keys
    - model: Ollama model name to use
    - temperature: Temperature for generation (0.0 to 1.0)
    - stream: Whether to stream the response
    - response_format: Optional format specification for JSON responses
    
    Returns:
    - String response or JSON object if response_format is specified
    """
    try:
        print_lg(f"Generating completion using Ollama model: {model}")
        
        # Convert OpenAI-style messages to Ollama format
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt = f"{content}\n\n{prompt}"
            elif role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        
        # Add final prompt marker
        prompt += "Assistant: "
        
        # Prepare the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature
            }
        }
        
        # Make the API request
        if stream:
            print_lg("--STREAMING STARTED")
            response = requests.post(
                f"{ollama_api_url}/api/generate", 
                json=payload,
                stream=True
            )
            
            result = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    chunk_text = chunk.get("response", "")
                    result += chunk_text
                    print_lg(chunk_text, end="", flush=True)
                    
                    # Check if we've reached the end of the stream
                    if chunk.get("done", False):
                        break
                        
            print_lg("\n--STREAMING COMPLETE")
        else:
            response = requests.post(
                f"{ollama_api_url}/api/generate", 
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "")
            else:
                error_msg = f"Ollama API error: {response.status_code} - {response.text}"
                print_lg(error_msg)
                raise Exception(error_msg)
        
        # Handle JSON response format if specified
        if response_format and response_format.get("type") == "json_schema":
            try:
                # Try to extract JSON from the response
                json_start = result.find("{")
                json_end = result.rfind("}") + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # If no JSON found, try to parse the whole response
                    result = json.loads(result)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to convert the text to JSON
                result = convert_to_json(result)
        
        print_lg("\nOllama Answer to Question:\n")
        print_lg(result, pretty=bool(response_format))
        return result
        
    except Exception as e:
        error_msg = f"Error occurred while generating Ollama completion: {str(e)}"
        ollama_error_alert(error_msg, e)
        return {"error": error_msg}

# Function to extract skills from job description using Ollama
def ollama_extract_skills(job_description: str, stream: bool = stream_output) -> Dict:
    """
    Function to extract skills from job description using Ollama.
    
    Parameters:
    - job_description: The job description text
    - stream: Whether to stream the response
    
    Returns:
    - Dictionary containing extracted skills
    """
    print_lg("-- EXTRACTING SKILLS FROM JOB DESCRIPTION USING OLLAMA")
    try:
        prompt = extract_skills_prompt.format(job_description)
        
        messages = [{"role": "user", "content": prompt}]
        return ollama_completion(
            messages, 
            model=ollama_model,
            stream=stream,
            response_format=extract_skills_response_format
        )
    except Exception as e:
        error_msg = f"Error occurred while extracting skills from job description using Ollama: {str(e)}"
        ollama_error_alert(error_msg, e)
        return {"error": error_msg}

# Function to answer questions using Ollama
def ollama_answer_question(
    question: str, 
    options: List[str] = None, 
    question_type: Literal['text', 'textarea', 'single_select', 'multiple_select'] = 'text',
    job_description: str = None, 
    about_company: str = None, 
    user_information_all: str = None,
    stream: bool = stream_output
) -> str:
    """
    Function to generate Ollama-based answers for questions in a form.
    
    Parameters:
    - question: The question being answered
    - options: List of options (for single_select or multiple_select questions)
    - question_type: Type of question (text, textarea, single_select, multiple_select)
    - job_description: Optional job description for context
    - about_company: Optional company details for context
    - user_information_all: Information about the user
    - stream: Whether to stream the response
    
    Returns:
    - The Ollama-generated answer
    """
    print_lg("-- ANSWERING QUESTION USING OLLAMA")
    try:
        prompt = ai_answer_prompt.format(user_information_all or "N/A", question)
        
        # Append optional details if provided
        if job_description and job_description != "Unknown":
            prompt += f"\nJob Description:\n{job_description}"
        if about_company and about_company != "Unknown":
            prompt += f"\nAbout the Company:\n{about_company}"
            
        # Add options if provided
        if options and (question_type == 'single_select' or question_type == 'multiple_select'):
            prompt += f"\nOptions: {', '.join(options)}"
            
        messages = [{"role": "user", "content": prompt}]
        print_lg("Prompt we are passing to Ollama: ", prompt)
        
        response = ollama_completion(
            messages,
            model=ollama_model,
            stream=stream
        )
        
        return response
    except Exception as e:
        error_msg = f"Error occurred while answering question using Ollama: {str(e)}"
        ollama_error_alert(error_msg, e)
        return "Error generating answer"
