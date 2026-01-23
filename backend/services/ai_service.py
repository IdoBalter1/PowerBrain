
import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
from ai_prompt import initial_prompt
from calendar_service import get_events,create_event, get_calendar_service
# Load .env from parent directory
load_dotenv(Path(__file__).parent.parent / ".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")

# Get the system message content (the string)
system_content = initial_prompt[0]["content"]

# Encode the string
tokens = encoding.encode(system_content)
print(f"Token count: {len(tokens)}")




def create_prompt(user_message: str, maxdays: int = 30) -> str:
    calendar_events = get_events(maxdays=maxdays)
    
    # Format calendar events for the AI prompt
    if calendar_events:
        events_text = "\n".join([
            f"- {event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'Unknown'))} to "
            f"{event.get('end', {}).get('dateTime', event.get('end', {}).get('date', 'Unknown'))}: "
            f"{event.get('summary', 'No title')}"
            for event in calendar_events
        ])
    else:
        events_text = "No existing calendar events found."
    
    prompt = f"""You are helping schedule learning blocks for the user's learning goal.

USER'S LEARNING REQUEST:
{user_message}

EXISTING CALENDAR EVENTS (DO NOT SCHEDULE OVER THESE):
{events_text}

INSTRUCTIONS:
1. Analyze the user's learning request and break it down into learning blocks
2. Schedule learning blocks around the existing calendar events shown above
3. Do NOT schedule any learning blocks at times that conflict with existing events
4. Leave reasonable breaks between learning sessions (at least 30 minutes between blocks)
5. Consider optimal learning times (morning hours are often better for focused learning)
6. Spread learning blocks across multiple days if needed

CALENDAR EVENT FORMAT:
When creating calendar events, use this exact structure:
{{
    "summary": "Learning: [Block Title]",
    "start": {{
        "dateTime": "[ISO 8601 datetime string]",
        "timeZone": "Europe/London"
    }},
    "end": {{
        "dateTime": "[ISO 8601 datetime string]",
        "timeZone": "Europe/London"
    }},
    "description": "[Detailed description of what to learn in this block]"
}}

IMPORTANT:
- All datetimes must be in ISO 8601 format (e.g., "2026-01-23T10:00:00Z")
- All times should be in Europe/London timezone
- Ensure start_time is before end_time
- Each learning block should be 30-120 minutes long
- Return the scheduled events as a JSON array of event objects

Please create a schedule of learning blocks that works around the user's existing commitments."""
    
    return prompt

def create_objective_from_request(request,username):

    prompt = create_prompt(request)
    initial_prompt.append({"role" : "user", "content":prompt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=initial_prompt,
        response_format={"type": "json_object"} 
    )

    return response

def create_events_from_ai_response(ai_response):
    """Create calendar events from AI response JSON"""
    import json
    
    # Parse response
    if hasattr(ai_response, 'choices'):
        data = json.loads(ai_response.choices[0].message.content)
    elif isinstance(ai_response, str):
        data = json.loads(ai_response)
    else:
        data = ai_response
    
    blocks = data.get("blocks", [])
    objective_title = data.get("objective", {}).get("title", "Learning")
    
    created = []
    service = get_calendar_service()
    
    for block in blocks:
        if not (block.get("start_time") and block.get("end_time")):
            continue
            
        event = {
            "summary": f"Learning: {block['title']}",
            "start": {"dateTime": block["start_time"], "timeZone": "Europe/London"},
            "end": {"dateTime": block["end_time"], "timeZone": "Europe/London"},
            "description": f"{objective_title}\n\n{block.get('subtitle', '')}"
        }
        
        try:
            result = service.events().insert(calendarId="primary", body=event).execute()
            created.append({"block": block, "event_id": result.get("id")})
            print(f"✅ Created: {block['title']}")
        except Exception as e:
            print(f"❌ Failed: {block['title']} - {e}")
    
    return created


def ask_clarifying_questions(request):
    # First call: AI asks questions
    pass
    
def create_objective_from_conversation(conversation_history):
    pass
if __name__ == "__main__":

    # Step 1: Create learning plan with AI
    user_request = "I want to learn HTML basics in 3 days"
    username = "test_user"
    
    
    ai_response = create_objective_from_request(user_request, username)
    
    # Step 2: Parse and show the response
    import json
    response_data = json.loads(ai_response.choices[0].message.content)

    created_events = create_events_from_ai_response(ai_response)

    print(f"   Created {len(created_events)} calendar events")
    for i, event_info in enumerate(created_events, 1):
        print(f"   {i}. {event_info['block']['title']} - Event ID: {event_info['event_id']}")