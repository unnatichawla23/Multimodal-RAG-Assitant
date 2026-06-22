def process_user_query(question):
    """
    Cleans and validates the user question.

    Args:
        question (str): Raw question entered by the user.

    Returns:
        str: Cleaned question.
    """
    if not question:
        return ""

    cleaned_question = " ".join(question.split())

    return cleaned_question