FOLLOW_UP_PHRASES = [
    "explain more",
    "tell me more",
    "why",
    "how",
    "simplify it",
    "explain it",
    "on this",
    "about this",
    "generate mcqs on this",
    "quiz on this",
    "more details"
]


def is_follow_up(question):
    question = question.lower()

    return any(
        phrase in question
        for phrase in FOLLOW_UP_PHRASES
    )