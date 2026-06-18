from pypdf import PdfReader
from utils.text_cleaner import clean_text


def extract_text_from_pdf(file_path):
    """
    Extracts and cleans text from a PDF file page by page.

    Args:
        file_path (str): Path of the saved PDF file.

    Returns:
        list: A list of dictionaries containing page number and cleaned text.
    """
    reader = PdfReader(file_path)
    pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text()
        cleaned_text = clean_text(raw_text)

        if cleaned_text:
            pages_text.append(
                {
                    "page_number": page_number,
                    "text": cleaned_text
                }
            )

    return pages_text