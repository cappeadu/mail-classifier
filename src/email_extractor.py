import base64


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
                        "utf-8",
                        errors="replace",
                    )

            elif "parts" in part:
                body = get_email_body(part)

                if body:
                    return body

    elif payload.get("mimeType") == "text/plain":
        data = payload["body"].get("data")

        if data:
            return base64.urlsafe_b64decode(data).decode(
                "utf-8",
                errors="replace",
            )

    return ""


def extract_email(service, message_id):
    """
    Retrieve one Gmail message and convert it into
    a simple Python dictionary.
    """

    message = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full",
        )
        .execute()
    )

    headers = {h["name"]: h["value"] for h in message["payload"].get("headers", [])}

    return {
        "id": message_id,
        "sender": headers.get("From", ""),
        "subject": headers.get("Subject", ""),
        "date": headers.get("Date", ""),
        "body": get_email_body(message["payload"]),
    }
