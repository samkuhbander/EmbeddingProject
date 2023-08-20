# embedding.py
from FlagEmbedding import FlagModel


def embed_sentences(code_chunks):
    model = FlagModel("BAAI/bge-base-en")
    embeddings = model.encode(code_chunks)
    return embeddings
