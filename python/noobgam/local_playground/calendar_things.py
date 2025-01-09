from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

if __name__ == "__main__":
    oauth2_client_secret_file = 'F:\\Downloads\\noobgam_life.json'
    scopes = [
        'https://www.googleapis.com/auth/calendar.calendarlist.readonly',
        'https://www.googleapis.com/auth/calendar.events.readonly'
    ]

    flow = InstalledAppFlow.from_client_secrets_file(oauth2_client_secret_file, scopes)
    creds = flow.run_local_server(port=0)

    service = build('calendar', 'v3', credentials=creds)
    evs = service.events().list(
        calendarId='primary',
    ).execute()
    print(evs)