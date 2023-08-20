from concurrent.futures import ThreadPoolExecutor
import glob
import hashlib
from parsers import parse_file
from embedding import embed_sentences
from milvus_DB import connect_to_milvus, create_collection, create_index, does_collection_exist, insert_entities
from compare_code_chunks import compareFiles
from search import search_similar_entities

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
if does_collection_exist(): 
    print("Milvus_DB already exists")
    files = compareFiles()
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

query = "add together numbers"
search_similar_entities(milvus_DB, query)