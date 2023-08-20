import glob
import hashlib
from milvus_DB import drop_altered_file
from pymilvus import (
    Collection
)

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return int(file_hash.hexdigest(), 16) % 10**16

def compareFiles():
    collection = Collection("milvus_DB")      # Get an existing collection.
    collection.load()

    directory_path = 'ExampleProject/*'
    file_paths = glob.glob(directory_path)
    
    print("these are the files received by compare_file_hashes: " + str(file_paths))
    for file_path in file_paths:
        hashed_file = hash_file(file_path)
        if 1 == len(collection.query(
            expr = str(hashed_file) + " == file_hash",
            offset = 0,
            output_fields = ["file_hash"],
            limit = 1,
            )):
            print("found a match. hash: " + str(hashed_file) + " file: " + file_path)
            file_paths.remove(file_path)
            # drop_altered_file(str(hashed_file)) 
    return file_paths





    