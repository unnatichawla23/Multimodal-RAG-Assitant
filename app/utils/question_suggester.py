def generate_suggested_questions(mode):
    """
    Generates smart follow-up question suggestions
    based on the selected assistant mode.
    """

    suggestions = {
        "Study Mode": [
            "Explain this in simple terms.",
            "Generate 5 MCQs from this document.",
            "Create revision notes.",
            "Generate flashcards."
        ],

        "Research Mode": [
            "Explain the methodology.",
            "What are the key findings?",
            "What are the limitations?",
            "Compare this paper with another paper."
        ],

        "Career Mode": [
            "Review my resume.",
            "Generate interview questions.",
            "Identify skill gaps.",
            "Suggest resume improvements."
        ],

        "Image/Scanned Document Mode": [
            "Summarize this image.",
            "Extract important information.",
            "Explain the text in simple language.",
            "Generate questions from this document."
        ],

        "General Document Q&A Mode": [
            "Summarize this document.",
            "Explain this in simple terms.",
            "Generate practice questions.",
            "What are the key points?"
        ],

        "Document Comparison Mode": [
            "Summarize the differences.",
            "Which document is better?",
            "Highlight important changes.",
            "Create a comparison table."
        ]
    }

    return suggestions.get(
        mode,
        suggestions["General Document Q&A Mode"]
    )