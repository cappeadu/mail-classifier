import csv
import time

from src.email_extractor import extract_email
from src.gmail_client import create_gmail_service

OUTPUT_FILE = "data/emails.csv"
MAX_RESULTS = 500
DELAY_SECONDS = 0.5


def get_message_ids(service, max_results):
    """Get Gmail message IDs using pagination."""

    messages = []
    next_page_token = None

    while len(messages) < max_results:
        results = (
            service.users()
            .messages()
            .list(
                userId="me",
                maxResults=min(100, max_results - len(messages)),
                pageToken=next_page_token,
            )
            .execute()
        )

        messages.extend(results.get("messages", []))

        next_page_token = results.get("nextPageToken")

        if not next_page_token:
            break

    return messages[:max_results]


def main():
    service = create_gmail_service()

    print("Getting message IDs...")
    messages = get_message_ids(service, MAX_RESULTS)

    print(f"Found {len(messages)} message IDs.")
    print("Extracting emails...\n")

    emails = []

    for i, message in enumerate(messages, start=1):
        email = extract_email(
            service,
            message["id"],
        )

        emails.append(email)

        if i % 25 == 0:
            print(f"Processed {i}/{len(messages)} emails...")

        # Slow down requests to avoid Gmail rate limits.
        time.sleep(DELAY_SECONDS)

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

    print(f"\nSaved {len(emails)} emails to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
