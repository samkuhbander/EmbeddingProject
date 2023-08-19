import glob
import numpy as np
from parsers import parse_methods
from embedding import embed_sentences
from milvus_DB import connect_to_milvus, create_collection, create_index, insert_entities

directory_path = 'ExampleProject/*'

files = glob.glob(directory_path)

# Collecting embeddings for all the chunks
all_embeddings = []

for file_path in files:
    print(f"Parsing file: {file_path}")
    methods_or_chunks = parse_methods(file_path)
    embeddings = embed_sentences(methods_or_chunks)
    all_embeddings.extend(embeddings)

dim = 768
num_entities = len(all_embeddings)

connect_to_milvus()
milvus_DB = create_collection(dim)
insert_entities(milvus_DB, num_entities, all_embeddings)
create_index(milvus_DB)
print("Done adding entities to Milvus_DB")

# Load collection
milvus_DB.load()
