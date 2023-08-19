import time

import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

def insert_entities(all_embeddings):
    fmt = "\n=== {:30} ===\n"
    search_latency_fmt = "search latency = {:.4f}s"
    # num_entities, dim = 3000, 8

    #################################################################################
    # 1. connect to Milvus
    print(fmt.format("start connecting to Milvus"))
    connections.connect("default", host="localhost", port="19530")

    has = utility.has_collection("hello_milvus")
    print(f"Does collection hello_milvus exist in Milvus: {has}")

    dim = 768  # Embedding dimension
    num_entities = len(all_embeddings)  # Sequence Length
    #################################################################################
    # 2. create collection
    fields = [
        FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
        FieldSchema(name="random", dtype=DataType.DOUBLE),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]

    schema = CollectionSchema(fields, "introducing melvis 'milvus_DB'")

    print(fmt.format("Create collection 'milvus_DB'"))
    milvus_DB = Collection("milvus_DB", schema, consistency_level="Strong")

    ################################################################################
    # 3. insert data
    print(fmt.format("Start inserting entities"))
    entities = [
        [str(i) for i in range(num_entities)],
        np.random.random(num_entities).tolist(), # If you want to keep the random field
        all_embeddings
    ]

    insert_result = milvus_DB.insert(entities)

    milvus_DB.flush()
    print(f"Number of entities in Milvus_DB: {milvus_DB.num_entities}")