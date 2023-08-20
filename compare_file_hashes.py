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
    files = glob.glob(directory_path)
    
    check = 0
    ret = []

    for file in files:
        hashed_file = hash_file(file)
        if hashed_file == collection.query(
            expr = str(hashed_file) + " == file_hash",
            offset = 0,
            output_fields = ["file_hash"],
            limit = 1,
            ):
            check+=1
            ret.append(file)
            print("found a match")
    if check > 0:
        print(check + " altered files dropped from Milvus_DB")
    return ret





    