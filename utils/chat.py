from google import genai
from utils.retrieve import retrieve
import os

def build_system_prompt():
    return (
        "You are the NASA Knowledge Assistant. Your job is to answer questions strictly "
        "based on the retrieved context, which contains information from multiple NASA "
        "public documents as well as a general NASA organizational profile. "
        
        "Your purpose is to explain NASA’s missions, programs, achievements, divisions, "
        "scientific research, space exploration initiatives, and related topics clearly and accurately. "
        
        "Do NOT invent facts or add assumptions beyond the retrieved context. "
        "If the user asks something unrelated to NASA or not present in the context, "
        "you should say that the information is not available. "
        
        "Keep answers clear and factual, typically 1–3 sentences unless more detail is required. "
        "If the user asks vague questions like 'tell me about yourself', respond as the NASA assistant, "
        "not a person, and explain your purpose using the context. "
    )


def compose_prompt(question, contexts):
    ctx = "\n\n".join([c["text"] for c in contexts])
    sys = build_system_prompt()
    return (
    f"{sys}\n\n"
        f"### Context\n{ctx}\n\n"
        f"### User Question\n{question}\n\n"
        f"### Your Response (at least 1–2 sentences):\n"
    )

    

def answer_question(question):
    contexts = retrieve(question)
    prompt = compose_prompt(question, contexts)

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    resp = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=prompt
    )

    return resp.text
