import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection
)

def connect_to_milvus():
    print("\n=== start connecting to Milvus ===\n")
    connections.connect("default", host="localhost", port="19530")

def create_collection(dim):
    # If collection already exists, drop it
    if utility.has_collection("milvus_DB"):
        print("\n=== Collection 'milvus_DB' already exists. Dropping it ===\n")
        utility.drop_collection("milvus_DB")

    print("\n=== Create collection 'milvus_DB' ===\n")
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="random", dtype=DataType.DOUBLE),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="code_snippet", dtype=DataType.VARCHAR, max_length=10000)
    ]

    schema = CollectionSchema(fields, description="introducing melvis 'milvus_DB'")
    milvus_DB = Collection("milvus_DB", schema, consistency_level="Strong")
    return milvus_DB

def insert_entities(milvus_DB, num_entities, all_embeddings, all_code_snippets):
    print("\n=== Start inserting entities ===\n")
    entities = [
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

