import ollama
import json
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_testcases_tool(prompt: str, model: str = "llama3.2") -> str:
    """
    Deterministcally generates test cases from a prompt using Ollama.
    Returns: Markdown formatted string.
    """
    logging.info(f"Generating test cases for prompt: {prompt[:50]}... with model: {model}")
    
    system_prompt = (
        "You are a QA automation expert. "
        "Your task is to generate comprehensive test cases based on the user's input. "
        "You must output a strictly formatted JSON array. Do not output markdown code blocks. "
        "Each object in the array should have the following fields:\n"
        "- `id`: e.g., 'TC_001'\n"
        "- `type`: 'POSITIVE' or 'NEGATIVE'\n"
        "- `title`: The name of the test case\n"
        "- `steps`: An array of strings, each being a step.\n"
        "- `expected`: The expected result string.\n"
        "Example format: [{\"id\": \"TC_001\", \"type\": \"POSITIVE\", \"title\": \"...\", \"steps\": [\"Step 1\", \"Step 2\"], \"expected\": \"...\"}]"
    )
    
    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        
        content = response['message']['content']
        logging.info("Generation successful.")
        return content
        
    except Exception as e:
        logging.error(f"Generation failed: {e}")
        return f"Error: Failed to generate test cases. Please ensure Ollama is running.\n\nDetails: {str(e)}"

if __name__ == "__main__":
    # Test execution
    print(generate_testcases_tool("Login page verification"))
