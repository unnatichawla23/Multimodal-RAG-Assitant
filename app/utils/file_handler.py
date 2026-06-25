import os
from config import UPLOAD_FOLDER


def save_uploaded_file(uploaded_file):
    """
    Saves an uploaded file to the uploads folder.

    Args:
        uploaded_file: File uploaded through Streamlit file_uploader.

    Returns:
        str: Saved file path.
    """
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path