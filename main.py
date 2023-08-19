import glob
import numpy as np
from parsers import parse_methods
from embedding import embed_sentences
import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import time

directory_path = 'ExampleProject/*'
files = glob.glob(directory_path)

# Collecting embeddings for all the chunks
all_embeddings = []

for file_path in files:
    print(f"Parsing file: {file_path}")
    methods_or_chunks = parse_methods(file_path)
    embeddings = embed_sentences(methods_or_chunks)
    all_embeddings.extend(embeddings)
    for index, method_or_chunk in enumerate(methods_or_chunks):
        print(f"Chunk {index + 1}:")
        print(method_or_chunk)
        print("-" * 50)

fmt = "\n=== {:30} ===\n"
# Connect to Milvus
print(fmt.format("start connecting to Milvus"))
connections.connect("default", host="localhost", port="19530")

# Check if the collection exists and create if not
has = utility.has_collection("hello_milvus")
print(f"Does collection hello_milvus exist in Milvus: {has}")

dim = 768  # Embedding dimension
num_entities = 512  # Sequence Length

fields = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
    FieldSchema(name="random", dtype=DataType.DOUBLE),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)
]

schema = CollectionSchema(fields, "hello_milvus is the simplest demo to introduce the APIs")
hello_milvus = Collection("hello_milvus", schema, consistency_level="Strong")

# Start inserting entities
print(fmt.format("Start inserting entities"))
entities = [
    [str(i) for i in range(num_entities)],
    np.random.random(num_entities).tolist(), # If you want to keep the random field
    all_embeddings
]