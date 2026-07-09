import re
import streamlit as st


def display_quiz(answer):
    """
    Displays AI-generated quizzes in a clean format.
    Works with both:
    - Correct Answer: B
    - B (without label)
    """

    # Split each question
    questions = re.split(r"(?=##\s*Question\s+\d+)", answer)

    for question in questions:

        question = question.strip()

        if not question:
            continue

        lines = [line.strip() for line in question.split("\n") if line.strip()]

        question_title = ""
        question_text = ""
        options = []
        correct_answer = ""
        explanation = ""

        reading_options = False
        reading_explanation = False

        for line in lines:

            # Title
            if line.startswith("## Question"):
                question_title = line.replace("## ", "")

            # Skip labels
            elif line == "Question:":
                continue

            elif (
                not reading_options
                and not reading_explanation
                and not question_text
            ):
                question_text = line

            # Options section
            elif line == "Options:":
                reading_options = True

            # Normal format
            elif line.startswith("Correct Answer"):
                correct_answer = line.replace("Correct Answer:", "").strip()
                reading_options = False
                reading_explanation = False

            elif line.startswith("Explanation"):
                explanation = line.replace("Explanation:", "").strip()
                reading_explanation = True

            # Flexible format (Gemini Flash Lite)
            elif re.fullmatch(r"[ABCD]", line):
                correct_answer = line
                reading_options = False
                reading_explanation = True

            elif reading_options:
                options.append(line)

            elif reading_explanation:

                if "--------------------------------" in line:
                    continue

                if explanation:
                    explanation += " " + line
                else:
                    explanation = line

        st.markdown(f"### 📝 {question_title}")

        if question_text:
            st.write(question_text)

        for option in options:
            st.write(option)

        with st.expander("✅ Show Answer"):

            if correct_answer:
                st.success(f"Correct Answer: {correct_answer}")

            if explanation:
                st.info(explanation)

        st.divider()