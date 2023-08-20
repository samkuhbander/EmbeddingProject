import glob
import hashlib
from pymilvus import Collection
from milvus_DB import drop_altered_file


def hash_file(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return int(file_hash.hexdigest(), 16) % 10**16


def compareFiles():
    collection = Collection("milvus_DB")  # Get an existing collection.
    collection.load()

    directory_path = "ExampleProject/*"
    original_file_paths = glob.glob(directory_path)
    filtered_file_paths = []  # We'll store the unmatched files here

    for file_path in original_file_paths:
        hashed_file = hash_file(file_path)
        if (
            len(
                collection.query(
                    expr=str(hashed_file) + " == file_hash",
                    offset=0,
                    output_fields=["file_hash"],
                    limit=1,
                )
            )
            != 1
        ):
            # If not found in the collection, add to the filtered list
            filtered_file_paths.append(file_path)
        else:
            print("found a match. hash: " + str(hashed_file) + " file: " + file_path)
            # drop_altered_file(str(hashed_file))

    return filtered_file_paths
