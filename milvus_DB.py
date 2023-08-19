import time
import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

def connect_to_milvus():
    print("\n=== start connecting to Milvus ===\n")
    connections.connect("default", host="localhost", port="19530")
    has = utility.has_collection("hello_milvus")
    print(f"Does collection hello_milvus exist in Milvus: {has}")

def create_collection(dim):
    print("\n=== Create collection 'milvus_DB' ===\n")
    fields = [
        FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
        FieldSchema(name="random", dtype=DataType.DOUBLE),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]

    schema = CollectionSchema(fields, "introducing melvis 'milvus_DB'")
    milvus_DB = Collection("milvus_DB", schema, consistency_level="Strong")
    return milvus_DB

def insert_entities(milvus_DB, num_entities, all_embeddings):
    print("\n=== Start inserting entities ===\n")
    entities = [
        [str(i) for i in range(num_entities)],
        np.random.random(num_entities).tolist(),
        all_embeddings
    ]

    insert_result = milvus_DB.insert(entities)
    milvus_DB.flush()
    print(f"Number of entities in Milvus_DB: {milvus_DB.num_entities}")
