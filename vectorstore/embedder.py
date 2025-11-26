from dotenv import load_dotenv
load_dotenv()


from sentence_transformers import SentenceTransformer

model = SentenceTransformer('intfloat/multilingual-e5-large-instruct')

def embed(text: str):
    return model.encode(text, normalize_embeddings=True)