from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="YOUR_KEY_HERE")

prompt = PromptTemplate.from_template("""
You are a helpful customer support agent.

Here is the customer's support ticket:
Subject: {subject}
Description: {description}
Category: {category}

Answer in a polite and helpful way.
""")

def answer_node(state: dict) -> dict:
    subject = state.get("subject", "")
    description = state.get("description", "")
    category = state.get("category", "")
    formatted_prompt = prompt.format(subject=subject, description=description, category=category)

    response = llm.invoke(formatted_prompt)
    
    return {
        "answer": response.content.strip()
    }
