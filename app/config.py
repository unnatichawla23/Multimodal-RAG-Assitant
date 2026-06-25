"""
SkillSight AI Configuration File

This file contains all configurable constants used throughout the project.
Keeping them here makes the project easier to maintain, debug, and scale.
"""

# Project Information

PROJECT_NAME = "SkillSight AI"
PROJECT_VERSION = "1.0.0"

# Upload Settings

UPLOAD_FOLDER = "uploads"

SUPPORTED_FILE_TYPES = [
    "pdf",
    "png",
    "jpg",
    "jpeg"
]

# Text Chunking

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Embedding Model

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Gemini Model
# Note:
# Gemini 2.0 Flash has no free quota for many new projects.
# Gemini 2.5 Flash Lite is recommended for free-tier usage.

GEMINI_MODEL = "gemini-2.5-flash-lite"

# ChromaDB

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "skillsight_documents"

TOP_K_RESULTS = 5

# OCR

OCR_LANGUAGES = ["en"]

# UI

MAX_SOURCE_PREVIEW_LENGTH = 800
MAX_CHUNK_PREVIEW_LENGTH = 700