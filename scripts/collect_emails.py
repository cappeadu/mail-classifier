import csv

from src.email_extractor import extract_email
from src.gmail_client import create_gmail_service

OUTPUT_FILE = "data/emails.csv"
MAX_RESULTS = 100


def main():
    service = create_gmail_service()

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=MAX_RESULTS,
        )
        .execute()
    )

    messages = results.get("messages", [])

    print(f"Found {len(messages)} messages.")

    emails = []

    for message in messages:
        email = extract_email(
            service,
            message["id"],
        )

        emails.append(email)

    fieldnames = [
        "id",
        "sender",
        "subject",
        "date",
        "body",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(emails)

    print(f"Saved {len(emails)} emails to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
