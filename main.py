import glob
import numpy as np
from parsers import parse_methods
from embedding import embed_sentences
from milvus_DB import insert_entities
import numpy as np

directory_path = 'ExampleProject/*'

files = glob.glob(directory_path)

# Collecting embeddings for all the chunks
all_embeddings = []

for file_path in files:
    print(f"Parsing file: {file_path}")
    methods_or_chunks = parse_methods(file_path)
    embeddings = embed_sentences(methods_or_chunks)
    all_embeddings.extend(embeddings)

insert_entities(all_embeddings)
print("Done adding entities to Milvus_DB")