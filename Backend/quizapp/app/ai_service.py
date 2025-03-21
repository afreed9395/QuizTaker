import openai
from django.conf import settings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
# Set your API key: AIzaSyBx8wtWNhVz27CIbOxBIH1artPM8dBcRyk

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key= settings.API_KEY
    # other params...
)

def generate_feedback(question_text, selected_answer, correct_answer):
    prompt = (
        f"Provide a 50 words brief explanation for the following quiz question:\n\n"
        f"Question: {question_text}\n"
        f"Student's answer: {selected_answer}\n"
        f"Correct answer: {correct_answer}\n\n"
        "Explain why the correct answer is right and why the candidate's answer might be incorrect. "
       
    )
    
    try:
       
        explanation = llm.invoke(prompt).content
        
        return explanation
        
    except Exception as e:
        print("Error generating feedback:", e)
        return "Feedback is currently unavailable. Please try again later."
