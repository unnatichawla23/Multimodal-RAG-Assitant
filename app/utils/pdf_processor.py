from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file page by page.

    Args:
        file_path (str): Path of the saved PDF file.

    Returns:
        list: A list of dictionaries containing page number and extracted text.
    """
    reader = PdfReader(file_path)
    pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages_text.append(
                {
                    "page_number": page_number,
                    "text": text
                }
            )

    return pages_text