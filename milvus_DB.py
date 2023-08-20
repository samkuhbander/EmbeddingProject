import numpy as np
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)


def connect_to_milvus():
    print("\n=== start connecting to Milvus ===\n")
    connections.connect("default", host="localhost", port="19530")


def does_collection_exist():
    print("\n=== check if Milvus_DB exists ===\n")
    return utility.has_collection("milvus_DB")

def drop_unrepresented_files(current_file_hashes):
    collection_name = "milvus_DB"
    collection = Collection(collection_name)
    collection.load()  # Get an existing collection.
    
    # Form the expression for the query
    expr = "file_hash not in " + str(current_file_hashes)
    
    # Query the primary key values based on the expression
    query_results = collection.query(
        expr=expr,
        offset=0,
        output_fields=["pk"],
    )

    # Extract the primary key values from the query results
    ids = [result['pk'] for result in query_results]

    print("\n=== dropped unrepresented files. PKs = " + str(ids) + "===\n")
    
    # Delete the entities by the primary key values
    expr_delete = f"pk in {ids}"
    print(collection.delete(expr_delete))
    collection.flush()  # Optionally flush the changes

# this if for testing and reseting purposes
def drop_collection(collection_name):
    utility.drop_collection(collection_name)


def create_collection(dim):
    # if database exists, drop it
    # if does_db_exist():
    # print("\n=== Drop collection 'milvus_DB' ===\n")
    # utility.drop_collection("milvus_DB")

    print("\n=== Create collection 'milvus_DB' ===\n")
    fields = [
        FieldSchema(
            name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True
        ),  # set auto_id to True
        FieldSchema(name="random", dtype=DataType.DOUBLE),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="code_snippet", dtype=DataType.VARCHAR, max_length=10000),
        FieldSchema(name="file_hash", dtype=DataType.INT64),  # Field for file hash
        FieldSchema(name="file_path", dtype=DataType.VARCHAR, max_length=100),
    ]

    schema = CollectionSchema(fields, description="introducing melvis 'milvus_DB'")
    milvus_DB = Collection("milvus_DB", schema, consistency_level="Strong")
    return milvus_DB


def insert_entities(
    milvus_DB,
    num_entities,
    all_embeddings,
    all_code_snippets,
    all_file_hashes,
    all_file_paths,
):
    print("\n=== Start inserting entities ===\n")
    entities = [
        np.random.random(num_entities).tolist(),
        all_embeddings,
        all_code_snippets,
        all_file_hashes,
        all_file_paths,
    ]

    if num_entities > 0:
        insert_result = milvus_DB.insert(entities)
    else:
        print("No new files to add to Milvus_DB")
    milvus_DB.flush()
    print(f"Number of entities in Milvus_DB: {milvus_DB.num_entities}")


def create_index(collection, field_name="embeddings", metric_type="L2"):
    index_params = {
        "metric_type": metric_type,
    }
    collection.create_index(field_name, index_params)
    print(f"Index created for field {field_name} in collection.")
