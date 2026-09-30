import html
import re


def clean_text(text):
    """
    Clean email text before machine learning.
    """

    if not isinstance(text, str):
        return ""

    # Decode HTML entities such as &amp; and &nbsp;
    text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # Convert to lowercase
    text = text.lower()

    # Replace anything that is not a letter or number with a space
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
