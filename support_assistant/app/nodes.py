import os
from dotenv import load_dotenv
from groq import Groq
from app.retriever import retrieve
from app.prompt import build_prompt, build_general_prompt
from app.schemas import ResponseSchema
from pydantic import ValidationError


load_dotenv()

mock_llm = os.getenv("MOCK_LLM", "1")  # env returns as a string value
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intent_classifier_prompt  = """
You are an intent classifier.

Classify the user's question into exactly one of these categories:

1. policy_question
   - Questions about delivery
   - Returns
   - Refunds
   - Membership
   - Order tracking
   - Order cancellation
   - Gift cards
   - Support hours

2. general_question
   - Any question not related to the above topics.

Return exactly one label and nothing else.

Allowed labels:
- policy_question
- general_question

Do not provide any explanation.

Example:
Question: Where is my delivery?
Label: policy_question

Question: Tell me a joke.
Label: general_question
"""

def classify_intent(state):

    question = state['question']

    print("\n========== CLASSIFY INTENT ==========")
    print("Question:", question)
    print("MOCK_LLM:", mock_llm)

    # ---------------- MOCK MODE(without llm) ---------------- #
    if mock_llm == "1":

        lower_question = question.lower()
        keywords = ["delivery", "return", "refund", "membership", "tracking", "cancel", "gift card", "support hours"]

        print("Lowercase question:", lower_question)
        print("Checking keywords...")

        if any(keyword in lower_question for keyword in keywords):

            state["intent"] = "policy_question"
            print(f"Without LLM i.e. Mock_llm mode = {mock_llm} for intent clasified as {state['intent']}")

            return state
        else:
            state["intent"] = "general_question"
            print(f"Without LLM i.e. Mock_llm mode = {mock_llm} for intent clasified as {state['intent']}")

            return state
        
    # ---------------- REAL LLM MODE ---------------- #
    elif mock_llm == "0":

        print("Calling Groq for intent classification...")

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"system","content": intent_classifier_prompt },
                {"role":"user","content":question},
            ],
            temperature=0
        )
        label = response.choices[0].message.content.strip()

        if label not in ["policy_question", "general_question"]:
            print("Invalid LLM label. Changing to general_question")
            label = "general_question"

        state["intent"] = label
        print(f"With LLM i.e. Mock_llm mode = {mock_llm} for intent clasified as {state['intent']}")


        return state


# print(classify_intent("How can go to Delhi?"))

def retrieve_and_answer(state):

    question = state['question']

    print("\n========== RETRIEVE AND ANSWER ==========")
    print("Question:", question)
    print("Intent:", state["intent"])
    print("MOCK_LLM:", mock_llm)

    print("Calling retriever...")

    retrived_documents = retrieve(question,top_k=3)  # embeds the query and retrive top-3
    documents = retrived_documents["documents"]
    sources = retrived_documents["ids"]   # contains all the ids

    print("Retrieved documents:", len(documents))
    print("Retrieved sources:", sources)

    for i, (doc, source) in enumerate(zip(documents, sources), 1):
        print(f"\nRetrieved Document {i}")
        print("Source:", source)
        print("Content:", doc[:200])

    # ---------------- MOCK MODE(without llm) ---------------- #
    if mock_llm == "1":
        print(f"Retrived answer for {state['intent']} without LLM i.e. Mock_llm mode = {mock_llm}")

        top_chunk = documents[0]
        top_chunk_snippet = top_chunk[:200]
        answer = f"Based on the retrieved context:\n\n{top_chunk_snippet}"
        state["answer"] = answer
        state["sources"] = sources
        state["confidence"] = 1.0

        print("Answer generated from top chunk")
        print("Sources:", state["sources"])
        print("Confidence:", state["confidence"])

        return state
  
    # ---------------- REAL LLM MODE ---------------- #
    elif mock_llm == "0":
        print(f"Retrived answer for {state['intent']} with LLM i.e. Mock_llm mode = {mock_llm}")

        context = "\n\n".join(documents)

        print("Context sent to LLM:")
        print(context[:500])

        rag_prompt = build_prompt(context=context,question=question)
        for attempt in range(3):

            print(f"\nLLM attempt: {attempt + 1}")

            try:
                response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role":"user","content": rag_prompt}
                ],
                    temperature=0.2
                )
                raw_output = response.choices[0].message.content.strip()

                print("Raw LLM output:")
                print(raw_output)

                # we need to validate with pydantic model because it strictly follows the schema 
                # As llm will not alwasy follow the rules to output the json format, so we validate it externally
                validated = ResponseSchema.model_validate_json(raw_output)  

                print("JSON validation successful")

                state["answer"] = validated.answer
                state["sources"] = sources
                state["confidence"] = validated.confidence

                print("Final answer:", state["answer"])
                print("Final sources:", state["sources"])
                print("Final confidence:", state["confidence"])

                return state
        

            except ValidationError as e:

                print("JSON validation FAILED")
                print("Validation error:", e)

                if attempt < 2:
                    rag_prompt += """
                    Your previous response was not valid JSON.
                    Return ONLY valid JSON matching the required schema.
                    Do not include any extra text.
                    """

        print("All 3 LLM attempts failed")

        state["answer"] = "ERROR: Failed to generate valid JSON."
        state["sources"] = []
        state["confidence"] = 0.0
        return state
    
    else:
        raise ValueError(
            f"Invalid MOCK_LLM value: {mock_llm}. Expected '0' or '1'."
        )


# for general questions
def direct_answer(state):

    question = state["question"]

    
    print("\n========== DIRECT ANSWER ==========")
    print("Question:", question)
    print("Intent:", state["intent"])
    print("MOCK_LLM:", mock_llm)

    # ---------------- MOCK MODE(without llm) ---------------- #
    if mock_llm == "1":
        print(f"Retrived answer for {state['intent']} without LLM i.e. Mock_llm = {mock_llm}")

        state["answer"] = "I can only answer questions about Zepto policies right now."
        state["sources"] = []
        state["confidence"] = 1.0

        print("Sources:", state["sources"])
        print("Confidence:", state["confidence"])

        return state

    # ---------------- REAL LLM MODE ---------------- #
    elif mock_llm == "0":
        print(f"Retrived answer for {state['intent']} with LLM i.e. Mock_llm mode = {mock_llm}")

        prompt = build_general_prompt(
            question=question
        )

        for attempt in range(3):

            print(f"\nLLM attempt: {attempt + 1}")

            try:

                response = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2
                )

                raw_output = response.choices[0].message.content.strip()

                print("Raw LLM output:")
                print(raw_output)

                validated = ResponseSchema.model_validate_json(raw_output)

                print("JSON validation successful")

                state["answer"] = validated.answer
                state["sources"] = []          # General questions never have sources
                state["confidence"] = validated.confidence

                return state

            except ValidationError as e:

                print(f"Validation failed (attempt {attempt + 1}): {e}")

                print("JSON validation FAILED")
                print("Validation error:", e)

                if attempt < 2:

                    print("Retrying with corrective instruction...")

                    prompt += """
                    Your previous response was not valid JSON.
                    Return ONLY valid JSON matching exactly this schema:
                    {
                        "answer": "...",
                        "sources": [],
                        "confidence": 0.95
                    }

                    Do not include markdown, explanations, or any extra text.
                    """
        print("All 3 LLm attempts failed")
        
        state["answer"] = "ERROR: Failed to generate valid JSON."
        state["sources"] = []
        state["confidence"] = 0.0

        return state
    
    else:
        raise ValueError(
            f"Invalid MOCK_LLM value: {mock_llm}. Expected '0' or '1'."
        )




