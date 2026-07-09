def get_mode_instructions(mode):
    """
    Returns mode-specific instructions for SkillSight AI.
    """
    instructions = {
        "Study Mode": """
You are in Study Mode.
Your answer should help a student understand and revise the material.

Response style:
- Explain concepts in simple language.
- Use short headings.
- Include key points.
- If useful, add revision notes.
- If the user asks for practice, generate MCQs or flashcards.
""",

        "Research Mode": """
You are in Research Mode.
Your answer should help with academic and research understanding.

Response style:
- Identify abstract, methodology, results, and conclusion when relevant.
- Highlight key findings.
- Mention research gaps if they appear in the context.
- Use a formal academic tone.
- If comparing papers, organize the comparison clearly.
""",

        "Career Mode": """
You are in Career Mode.
Your answer should help with resumes, job descriptions, skills, and interviews.

Response style:
- Compare resume and job description when relevant.
- Identify skill gaps.
- Suggest resume improvements.
- Generate interview questions when useful.
- Keep advice practical and career-focused.
""",

        "Image/Scanned Document Mode": """
You are in Image/Scanned Document Mode.
Your answer should help explain text extracted from images, screenshots, or scanned documents.

Response style:
- Explain what the extracted text means.
- Mention if the text seems incomplete or unclear.
- Summarize visible information.
- Keep the explanation simple and direct.
""",

        "General Document Q&A Mode": """
You are in General Document Q&A Mode.
Your answer should directly answer the user's question using the uploaded document context.

Response style:
- Be clear and concise.
- Use source-grounded explanations.
- Mention page numbers where relevant.
- Avoid unnecessary extra information.
"""
    }

    return instructions.get(mode, instructions["General Document Q&A Mode"])


def build_rag_prompt(question, retrieved_chunks, mode):
    """
    Builds a structured RAG prompt using the user question,
    retrieved document chunks, and selected assistant mode.
    """
    context_blocks = []

    for chunk in retrieved_chunks:
        context_blocks.append(
            f"Source: {chunk['document_name']}, "
            f"Page: {chunk['page_number']}, "
            f"Chunk: {chunk['chunk_index']}\n"
            f"Content: {chunk['chunk_text']}"
        )

    context = "\n\n".join(context_blocks)
    mode_instructions = get_mode_instructions(mode)

    prompt = f"""
You are SkillSight AI, a multimodal RAG-based Student and Career Assistant.

Selected Mode:
{mode}

Mode-Specific Instructions:
{mode_instructions}

Core Rules:
1. Use ONLY the provided document context.
2. Do not use outside knowledge.
3. If the answer is not found in the context, say: "The answer is not available in the uploaded document."
4. Mention source page numbers wherever relevant.
5. Do not hallucinate or invent information.
6. Keep the answer useful for students and early-career professionals.
7. If the user asks to generate a quiz, MCQs, practice questions, interview questions, or viva questions, create them ONLY from the provided document context.
8. If generating MCQs, ALWAYS return the quiz using EXACTLY the following format.

## Question 1

Question:
<question>

Options:
A. <option>
B. <option>
C. <option>
D. <option>

Correct Answer:
A

Explanation:
<one short explanation>

------------------------

## Question 2

Question:
...

Options:
A.
B.
C.
D.

Correct Answer:
B

Explanation:
...

Repeat this exact structure for every question.

Never omit the labels "Correct Answer:" or "Explanation:".
Never replace them with any other wording.
9. If generating interview questions or viva questions, return them as a numbered list with each question on its own line.

User Question:
{question}

Document Context:
{context}

Final Answer:
"""

    return prompt.strip()

def build_quiz_prompt(question, retrieved_chunks, mode):
    """
    Builds a dedicated prompt for quiz generation.
    """

    context_blocks = []

    for chunk in retrieved_chunks:
        context_blocks.append(
            f"Source: {chunk['document_name']}, "
            f"Page: {chunk['page_number']}, "
            f"Chunk: {chunk['chunk_index']}\n"
            f"Content: {chunk['chunk_text']}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are SkillSight AI.

Your task is ONLY to generate quizzes.

Use ONLY the document context.

Never use outside knowledge.

If the answer is unavailable in the document, do not create a question about it.

Generate the quiz using EXACTLY this format.

## Question 1

Question:
...

Options:
A. ...
B. ...
C. ...
D. ...

Correct Answer:
A

Explanation:
...

--------------------------------

Repeat this format for every question.

Do NOT skip any headings.

Do NOT replace the heading names.

User Request:
{question}

Document Context:
{context}

Quiz:
"""

    return prompt.strip()