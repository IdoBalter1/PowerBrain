
import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
from ai_prompt import messages
# Load .env from parent directory
load_dotenv(Path(__file__).parent.parent / ".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")

# Get the system message content (the string)
system_content = messages[0]["content"]

# Encode the string
tokens = encoding.encode(system_content)
print(f"Token count: {len(tokens)}")





#print(response.output_text)

def create_objective_from_request(request,username):
    messages.append({"role" : "user", "content":request})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"} 
    )
    

    return response

def ask_clarifying_questions(request):
    # First call: AI asks questions
    pass
    
def create_objective_from_conversation(conversation_history):
    pass
