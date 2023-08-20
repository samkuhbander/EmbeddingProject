import glob
import hashlib
from milvus_DB import drop_altered_file, drop_unrepresented_files
from pymilvus import (
    Collection
)

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return int(file_hash.hexdigest(), 16) % 10**16

def drop_files_helper(file_paths):
    print("these are the files received by drop_files_helper: " + str(file_paths))
    for file_path in file_paths:
        drop_altered_file(file_path)

def compareFiles():
    collection = Collection("milvus_DB")      # Get an existing collection.
    collection.load()

    directory_path = 'ExampleProject/*'
    file_paths = glob.glob(directory_path)
    current_hashed_files = []

    print("these are the files received by compare_file_hashes: " + str(file_paths))
    for file_path in file_paths:
        hashed_file = hash_file(file_path)
        current_hashed_files.append(hashed_file)

        if 1 == len(collection.query(
            expr = str(hashed_file) + " == file_hash",
            offset = 0,
            output_fields = ["file_hash"],
            limit = 1,
            )):
            print("found a match. hash: " + str(hashed_file) + " file: " + file_path)
            file_paths.remove(file_path)


    print("exited for loop")
    # drop_files_helper(file_paths)
    drop_unrepresented_files(current_hashed_files)
    return file_paths





    