from sentence_transformers import SentenceTransformer
import torch

# Load the model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

def get_similarity(queries, documents):
    # Encode the queries and documents. Note that queries benefit from using a prompt
    query_embeddings = model.encode(queries, prompt_name="query")
    document_embeddings = model.encode(documents)
    
    # Compute the (cosine) similarity between the query and document embeddings
    similarity = model.similarity(query_embeddings, document_embeddings)
    return similarity

def embed_query(queries):
    query_embeddings = model.encode(queries, prompt_name="query")
    return query_embeddings

def embed_document(documents):
    document_embeddings = model.encode(documents)
    return document_embeddings

def retrieve_best_document(queries, documents, similarities):
    similarity_matrix = similarities 
    retrieved_results = []
    
    for i, scores_for_query in enumerate(similarity_matrix):
        best_match_index = torch.argmax(scores_for_query).item()
        best_document_text = documents[best_match_index]
        best_score = scores_for_query[best_match_index].item()

        retrieved_results.append({
            "query": queries[i],
            "best_document": best_document_text,
            "score": best_score
        })

    return retrieved_results
