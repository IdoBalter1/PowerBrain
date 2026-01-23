import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

SERVICE_DIR = Path(__file__).parent
def get_calendar_service():
    creds = None
    token_path = SERVICE_DIR / "token.json"
    credentials_path = SERVICE_DIR / "credentials.json"
    
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"credentials.json not found at {credentials_path}. "
                    "Please download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    return build("calendar", "v3", credentials=creds)


def get_events(maxdays):
  try:
    service = get_calendar_service()
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    max_days_later = now + datetime.timedelta(days = maxdays)
    time_min = now.isoformat()
    time_max = max_days_later.isoformat()
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax = time_max,
            maxResults=1000,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return []

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
    return events

  except HttpError as error:
    print(f"An error occurred: {error}")
    return []
  

def create_event(summary, start_time, end_time, description=None, location=None):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("calendar", "v3", credentials=creds)
    event = {
        "summary": summary,
        "start": {
            "dateTime": start_time,
            "timeZone": "Europe/London",  
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Europe/London",   
        }
    }
    if description:
        event["description"] = description
    if location:
        event["location"] = location

    try:
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")
        return created_event
    except Exception as e:
        print(f"An error occurred creating the event: {e}")
        return None
      



if __name__ == "__main__":
  user_message = 'I want to learn HTML in 10 days for my interview'
  maxdays = 30
  print(create_prompt(user_message, maxdays))
  # Example usage: create an event
  