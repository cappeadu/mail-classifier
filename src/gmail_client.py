from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def create_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",
        SCOPES,
    )

    credentials = flow.run_local_server(
        port=0,
        open_browser=True,
    )

    return build(
        "gmail",
        "v1",
        credentials=credentials,
    )
