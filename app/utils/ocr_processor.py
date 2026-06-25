import easyocr
from config import OCR_LANGUAGES

reader = easyocr.Reader(OCR_LANGUAGES)


def extract_text_from_image(image_path):
    """
    Extracts text from an image using EasyOCR.

    Args:
        image_path (str): Path of the uploaded image.

    Returns:
        list: OCR text structured similarly to PDF pages.
    """
    results = reader.readtext(image_path, detail=0)

    extracted_text = " ".join(results)

    return [
        {
            "page_number": 1,
            "text": extracted_text
        }
    ]