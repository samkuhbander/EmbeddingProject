import glob
from parsers import parse_methods
from embedding import embed_sentences
from milvus_DB import connect_to_milvus, create_collection, create_index, insert_entities

directory_path = 'ExampleProject/*'

files = glob.glob(directory_path)

# Collecting embeddings for all the chunks
all_embeddings = []
all_code_snippets = []

for file_path in files:
    print(f"Parsing file: {file_path}")
    methods_or_chunks = parse_methods(file_path)
    embeddings = embed_sentences(methods_or_chunks)
    all_embeddings.extend(embeddings)
    all_code_snippets.extend(methods_or_chunks)

dim = 768
num_entities = len(all_embeddings)

connect_to_milvus()
milvus_DB = create_collection(dim)
insert_entities(milvus_DB, num_entities, all_embeddings, all_code_snippets)
create_index(milvus_DB)
print("Done adding entities to Milvus_DB")

# Load collection
milvus_DB.load()

# Search for similar entities
query = "add together numbers"
query_embedding = [embed_sentences([query])[0]]
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = milvus_DB.search(query_embedding, "embeddings", search_params, limit=3)

# Get IDs and perform query
ids_to_query = [hit.id for hit in results[0]]
query_results = milvus_DB.query(f"pk in {ids_to_query}", output_fields=["code_snippet"])

# Print results
print("Search Results for " + query + ":")
for hit, code_snippet in zip(results[0], query_results):
    print(f"ID: {hit.id}, Distance: {hit.distance}")
    print("Code Snippet:")
    print(code_snippet['code_snippet'] + "\n")
