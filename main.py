from concurrent.futures import ThreadPoolExecutor
import glob
import hashlib
from parsers import parse_file
from embedding import embed_sentences
from milvus_DB import connect_to_milvus, create_collection, create_index, does_collection_exist, insert_entities
from compare_code_chunks import compareFiles

def process_file(file_path):
    print(f"Parsing file: {file_path}")
    methods_or_chunks = parse_file(file_path)
    embeddings = embed_sentences(methods_or_chunks)
    file_hash = hash_file(file_path)
    return embeddings, methods_or_chunks, file_hash

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return int(file_hash.hexdigest(), 16) % 10**16

dim = 768

directory_path = ''
files = None
milvus_DB = None
connect_to_milvus()
if does_collection_exist():  # temporarily make this code unreachable
    # only add the new embeddings and code snippets
    print("Milvus_DB already exists")
    files = compareFiles(); # TODO: this is where we extract the new files
    if len(files) == 0:
        print("No new files to add to Milvus_DB")
    milvus_DB = create_collection(dim)
else:
    print("Milvus_DB does not exist")
    milvus_DB = create_collection(dim)
    directory_path = 'ExampleProject/*'
    files = glob.glob(directory_path)


# Collecting embeddings for all the chunks
all_embeddings = []
all_code_snippets = []
all_file_hashes = []

with ThreadPoolExecutor() as executor:
    results = list(executor.map(process_file, files))

for embeddings, methods_or_chunks, file_hash in results:
    all_embeddings.extend(embeddings)
    all_code_snippets.extend(methods_or_chunks)
    all_file_hashes.extend([file_hash] * len(methods_or_chunks))

num_entities = len(all_embeddings)

insert_entities(milvus_DB, num_entities, all_embeddings, all_code_snippets, all_file_hashes)
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
