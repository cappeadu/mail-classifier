from src.email_extractor import extract_email
from src.gmail_client import create_gmail_service


def main():
    service = create_gmail_service()

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=10,
        )
        .execute()
    )

    messages = results.get("messages", [])

    print(f"Found {len(messages)} messages.\n")

    for message in messages:
        email = extract_email(
            service,
            message["id"],
        )

        print("=" * 80)
        print("ID:", email["id"])
        print("From:", email["sender"])
        print("Subject:", email["subject"])
        print("Date:", email["date"])
        print("\nBODY:")
        print(email["body"][:500])
        print()


if __name__ == "__main__":
    main()
