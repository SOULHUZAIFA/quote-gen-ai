import os
import openai
from pathlib import Path

# Validate environment variables
def validate_env():
    api_key = "sk-0ecdb8d1f6214c16ad76082bf920637c"
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY environment variable not set")
    return api_key

# Load prompt template with proper path handling
def load_prompt_template():
    prompt_path = Path(__file__).parent.parent / "prompts" / "generate_quote.txt"
    try:
        with open(prompt_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt template not found at {prompt_path}")

# Generate a quote using DeepSeek API
def generate_quote(customer_input):
    if not customer_input or not isinstance(customer_input, str):
        raise ValueError("Customer input must be a non-empty string")

    try:
        prompt_template = load_prompt_template()
        full_prompt = f"{prompt_template}\n\nCustomer input: \"{customer_input}\""

        openai.api_base = "https://api.deepseek.com/v1"
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a sign company."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        raise Exception(f"Failed to generate quote: {str(e)}")

# Main execution
if __name__ == "__main__":
    try:
        openai.api_key = validate_env()
        customer_request = input("Enter customer quote request: ").strip()
        if not customer_request:
            print("Error: Quote request cannot be empty")
            exit(1)

        print("\nGenerating quote...\n")
        quote = generate_quote(customer_request)
        print(quote)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
