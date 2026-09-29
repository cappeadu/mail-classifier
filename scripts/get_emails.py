import base64

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_email_body(payload):
    """
    Extract plain-text body from a Gmail message payload.
    """

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")

                if data:
                    return base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="replace"
                    )

            elif "parts" in part:
                body = get_email_body(part)

                if body:
                    return body

    elif payload.get("mimeType") == "text/plain":
        data = payload["body"].get("data")

        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    return ""


def main():

    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)

    credentials = flow.run_local_server(port=0, open_browser=True)

    service = build("gmail", "v1", credentials=credentials)

    results = service.users().messages().list(userId="me", maxResults=10).execute()

    messages = results.get("messages", [])

    print(f"\nFound {len(messages)} messages.\n")

    for message in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message["id"], format="full")
            .execute()
        )

        headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}

        body = get_email_body(msg["payload"])

        print("=" * 80)
        print("ID:", message["id"])
        print("From:", headers.get("From"))
        print("Subject:", headers.get("Subject"))
        print("Date:", headers.get("Date"))

        print("\nBODY:")
        print(body[:2000])
        print()


if __name__ == "__main__":
    main()
