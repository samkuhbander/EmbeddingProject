import glob
import numpy as np
from parsers import parse_methods
from embedding import embed_sentences
import csv

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

# Saving as a .csv file
with open('embeddings.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(all_embeddings)
    
