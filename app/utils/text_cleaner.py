import re


def clean_text(text):
    """
    Cleans extracted text by removing extra spaces,
    empty lines, and unnecessary whitespace.

    Args:
        text (str): Raw extracted text.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text