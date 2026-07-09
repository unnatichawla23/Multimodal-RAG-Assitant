import os
from dotenv import load_dotenv
from config import GEMINI_MODEL
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, NotFound


load_dotenv()


def generate_answer_with_gemini(prompt):
    """
    Generates an answer using Gemini based on the RAG prompt.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key not found. Please check your .env file."

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        return response.text

    except ResourceExhausted as error:
        return f"RESOURCE EXHAUSTED:\n\n{error}"

    except NotFound:
        return (
            "Selected Gemini model is not available for this API key/project. "
            "Please check available Gemini models in Google AI Studio."
        )

    except Exception as error:
        return f"Gemini error: {error}"