from sentence_transformers import SentenceTransformer

documents = [
    "Machine learning enables systems to learn from data",
    "Overfitting occurs when a model memorizes training data",
    "Vector databases enable fast similarity search"
]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents)

print("Documents embedded successfully")