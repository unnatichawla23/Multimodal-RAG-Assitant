def create_text_chunks(pages_text, document_name, chunk_size=800, chunk_overlap=150):
    """
    Splits cleaned page text into smaller chunks.

    Args:
        pages_text (list): List of dictionaries with page_number and text.
        document_name (str): Name of the uploaded document.
        chunk_size (int): Maximum characters per chunk.
        chunk_overlap (int): Overlap between chunks.

    Returns:
        list: List of chunk dictionaries with metadata.
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