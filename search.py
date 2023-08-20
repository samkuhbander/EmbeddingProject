from embedding import embed_sentences


def search_similar_entities(milvus_DB, query, limit=3):
    # Embed the query
    query_embedding = [embed_sentences([query])[0]]

    # Define search parameters
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

    # Perform the search
    results = milvus_DB.search(
        query_embedding, "embeddings", search_params, limit=limit
    )

    # Get IDs and perform query
    ids_to_query = [hit.id for hit in results[0]]
    query_results = milvus_DB.query(
        f"pk in {ids_to_query}", output_fields=["code_snippet"]
    )

    # Print results
    print("Search Results for " + query + ":")
    for hit, code_snippet in zip(results[0], query_results):
        print(f"ID: {hit.id}, Distance: {hit.distance}")
        print("Code Snippet:")
        print(code_snippet["code_snippet"] + "\n")

    return query_results
