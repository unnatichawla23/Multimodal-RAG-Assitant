from config import CHUNK_SIZE, CHUNK_OVERLAP


def create_text_chunks(
    pages_text,
    document_name,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
):
    """
    Splits cleaned page text into smaller chunks.
    """
    chunks = []
    chunk_index = 1

    for page in pages_text:
        page_number = page["page_number"]
        text = page["text"]

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append(
                {
                    "chunk_index": chunk_index,
                    "document_name": document_name,
                    "page_number": page_number,
                    "chunk_text": chunk_text
                }
            )

            chunk_index += 1
            start += chunk_size - chunk_overlap

    return chunks