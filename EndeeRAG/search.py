from sentence_transformers import SentenceTransformer
import numpy as np

documents = [
    "Machine learning enables systems to learn from data",
    "Overfitting occurs when a model memorizes training data",
    "Vector databases enable fast similarity search"
]

model = SentenceTransformer("all-MiniLM-L6-v2")
doc_vectors = model.encode(documents)

query = "What is overfitting?"
query_vector = model.encode([query])[0]

scores = np.dot(doc_vectors, query_vector)
best_match = scores.argmax()

print("Query:", query)
print("Best match:", documents[best_match])