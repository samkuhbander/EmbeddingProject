import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection
)
from hashlib import sha256

def connect_to_milvus():
    print("\n=== start connecting to Milvus ===\n")
    connections.connect("default", host="localhost", port="19530")

def does_db_exist():
    print("\n=== check if Milvus_DB exists ===\n")
    return utility.has_collection("milvus_DB")

def create_collection(dim):
    #if database exists, drop it
    if does_db_exist():
        print("\n=== Drop collection 'milvus_DB' ===\n")
        utility.drop_collection("milvus_DB")

    print("\n=== Create collection 'milvus_DB' ===\n")
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False), # set auto_id to False
        FieldSchema(name="random", dtype=DataType.DOUBLE),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="code_snippet", dtype=DataType.VARCHAR, max_length=10000)
    ]

    schema = CollectionSchema(fields, description="introducing melvis 'milvus_DB'")
    milvus_DB = Collection("milvus_DB", schema, consistency_level="Strong")
    return milvus_DB

def insert_entities(milvus_DB, num_entities, all_embeddings, all_code_snippets):
    print("\n=== Start inserting entities ===\n")
    pks = [int(sha256(snippet.encode()).hexdigest(), 16) % 10**16 for snippet in all_code_snippets] # Creating a hash as pk
    entities = [
        pks,
        np.random.random(num_entities).tolist(),
        all_embeddings,
        all_code_snippets
    ]

    insert_result = milvus_DB.insert(entities)
    milvus_DB.flush()
    print(f"Number of entities in Milvus_DB: {milvus_DB.num_entities}")

def create_index(collection, field_name="embeddings", metric_type="L2"):
    index_params = {
        "metric_type": metric_type,
    }
    collection.create_index(field_name, index_params)
    print(f"Index created for field {field_name} in collection.")

