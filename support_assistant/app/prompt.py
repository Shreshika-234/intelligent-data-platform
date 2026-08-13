def build_prompt(context,question):

    prompt = f"""
    Role:
    You are a friendly and professional customer support assistant for Zepto.
    
    Context:
    {context}

    Task:
    Question: {question}    
    - Answer the user's question using the provided context.

    Negative Constraint:
    - Do not answer using information that is not present in the provided context.
    - If the answer cannot be found in the context, reply:
      "I don't have enough information to answer this question."

    Format:
    Return ONLY valid JSON in exactly this format:

    {{
        "answer": "...",
        "sources": [],
        "confidence": 0.95
    }}

    Length:
    - Keep the answer between 3 and 5 sentences.

    Example:

    Context:
    Refunds are processed within 5 business days.

    Question:
    When will I receive my refund?

    Output:
    {{
        "answer": "Refunds are processed within 5 business days.",
        "sources": ["doc_02"],
        "confidence": 0.95
    }}

"""
    return prompt

def build_general_prompt(question):

    prompt = f"""
            Role:
            You are a friendly and professional AI assistant.

            Task:
            Answer the user's question accurately.

            Question:
            {question}

            Format:
            Return ONLY valid JSON.

            {{
                "answer": "...",
                "sources": [],
                "confidence": 0.95
            }}

            Length:
            Keep the answer between 3 and 5 sentences.
            """
    return prompt