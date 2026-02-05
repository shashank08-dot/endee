from langchain_openai import ChatOpenAI

context = "Overfitting happens when a model memorizes data instead of learning patterns."
question = "Explain overfitting"

llm = ChatOpenAI(temperature=0)

prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""

response = llm.invoke(prompt)
print(response.content)