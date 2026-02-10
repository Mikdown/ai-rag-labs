import os
import math
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

# Load environment variables
load_dotenv()

def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors
    Cosine similarity = (A · B) / (||A|| * ||B||)
    """
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensions")
    
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    
    return dot_product / (norm_a * norm_b)

def search_sentences(vector_store, query, k=3):
    """
    Search for similar sentences in the vector store
    
    Args:
        vector_store: The InMemoryVectorStore instance
        query: The search query string
        k: Number of results to return (default: 3)
    
    Returns:
        List of tuples containing (Document, similarity_score)
    """
    results = vector_store.similarity_search_with_score(query, k=k)
    
    print(f"\n=== Search Results for: \"{query}\" ===\n")
    
    for rank, (document, score) in enumerate(results, 1):
        print(f"{rank}. Score: {score:.4f} | {document.page_content}")
    
    return results

def hybrid_search(vector_store, query, k=3, vector_weight=0.7, keyword_weight=0.3):
    """
    Hybrid search combining vector similarity and keyword matching
    
    Args:
        vector_store: The InMemoryVectorStore instance
        query: The search query string
        k: Number of results to return (default: 3)
        vector_weight: Weight for vector similarity score (default: 0.7)
        keyword_weight: Weight for keyword matching score (default: 0.3)
    
    Returns:
        List of tuples containing (Document, hybrid_score)
    """
    # Get vector similarity results with a larger k to consider more candidates
    vector_results = vector_store.similarity_search_with_score(query, k=k*2)
    
    # Normalize query for keyword matching
    query_words = set(query.lower().split())
    
    # Calculate hybrid scores
    hybrid_results = []
    for document, vector_score in vector_results:
        # Calculate keyword matching score (0-1)
        doc_text = document.page_content.lower()
        doc_words = set(doc_text.split())
        
        # Count matching words
        matching_words = len(query_words.intersection(doc_words))
        keyword_score = matching_words / len(query_words) if query_words else 0
        
        # Combine scores
        hybrid_score = (vector_weight * vector_score) + (keyword_weight * keyword_score)
        hybrid_results.append((document, hybrid_score, vector_score, keyword_score))
    
    # Sort by hybrid score (descending)
    hybrid_results.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k results
    top_k = hybrid_results[:k]
    
    print(f"\n=== Hybrid Search Results for: \"{query}\" ===\n")
    print(f"(Vector Score Weight: {vector_weight}, Keyword Weight: {keyword_weight})\n")
    
    for rank, (document, hybrid_score, vector_score, keyword_score) in enumerate(top_k, 1):
        print(f"{rank}. Hybrid: {hybrid_score:.4f} | Vector: {vector_score:.4f} | Keyword: {keyword_score:.4f}")
        print(f"   Text: {document.page_content}\n")
    
    return top_k

def get_available_categories(vector_store):
    """
    Get available categories from the vector store metadata
    
    Args:
        vector_store: The InMemoryVectorStore instance
    
    Returns:
        Set of unique categories
    """
    categories = set()
    # Access the internal data structure to get all documents
    for doc_dict in vector_store.store.values():
        if 'metadata' in doc_dict and 'category' in doc_dict['metadata']:
            categories.add(doc_dict['metadata']['category'])
    return sorted(categories)

def search_by_category(vector_store, query, category, k=3):
    """
    Search for similar sentences within a specific category
    
    Args:
        vector_store: The InMemoryVectorStore instance
        query: The search query string
        category: The category to filter by
        k: Number of results to return (default: 3)
    
    Returns:
        List of tuples containing (Document, similarity_score)
    """
    # Use filter parameter for category-specific search
    filter_condition = {"category": category}
    results = vector_store.similarity_search_with_score(query, k=k, filter=filter_condition)
    
    print(f"\n=== Category Search Results for: \"{query}\" in '{category}' ===\n")
    
    if not results:
        print(f"❌ No results found in '{category}' category for query: \"{query}\"")
    else:
        for rank, (document, score) in enumerate(results, 1):
            print(f"{rank}. Score: {score:.4f} | {document.page_content}")
    
    return results

def hybrid_search_by_category(vector_store, query, category, k=3, vector_weight=0.7, keyword_weight=0.3):
    """
    Hybrid search within a specific category
    
    Args:
        vector_store: The InMemoryVectorStore instance
        query: The search query string
        category: The category to filter by
        k: Number of results to return (default: 3)
        vector_weight: Weight for vector similarity score (default: 0.7)
        keyword_weight: Weight for keyword matching score (default: 0.3)
    
    Returns:
        List of tuples containing (Document, hybrid_score)
    """
    # Get vector similarity results with category filter
    filter_condition = {"category": category}
    vector_results = vector_store.similarity_search_with_score(query, k=k*2, filter=filter_condition)
    
    # Normalize query for keyword matching
    query_words = set(query.lower().split())
    
    # Calculate hybrid scores
    hybrid_results = []
    for document, vector_score in vector_results:
        # Calculate keyword matching score (0-1)
        doc_text = document.page_content.lower()
        doc_words = set(doc_text.split())
        
        # Count matching words
        matching_words = len(query_words.intersection(doc_words))
        keyword_score = matching_words / len(query_words) if query_words else 0
        
        # Combine scores
        hybrid_score = (vector_weight * vector_score) + (keyword_weight * keyword_score)
        hybrid_results.append((document, hybrid_score, vector_score, keyword_score))
    
    # Sort by hybrid score (descending)
    hybrid_results.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k results
    top_k = hybrid_results[:k]
    
    print(f"\n=== Hybrid Category Search Results for: \"{query}\" in '{category}' ===\n")
    print(f"(Vector Score Weight: {vector_weight}, Keyword Weight: {keyword_weight})\n")
    
    if not top_k:
        print(f"❌ No results found in '{category}' category for query: \"{query}\"")
    else:
        for rank, (document, hybrid_score, vector_score, keyword_score) in enumerate(top_k, 1):
            print(f"{rank}. Hybrid: {hybrid_score:.4f} | Vector: {vector_score:.4f} | Keyword: {keyword_score:.4f}")
            print(f"   Text: {document.page_content}\n")
    
    return top_k

def load_document(vector_store, file_path):
    """
    Load a document from a file and add it to the vector store.
    
    Args:
        vector_store: The InMemoryVectorStore instance
        file_path: Path to the document file to load
    
    Returns:
        The document ID from the vector store
    
    Raises:
        FileNotFoundError: If the file does not exist
        Exception: For other I/O or processing errors
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content:
            print(f"⚠️  Warning: File '{os.path.basename(file_path)}' is empty")
        
        # Create Document object
        doc = Document(
            page_content=content,
            metadata={
                'fileName': os.path.basename(file_path),
                'createdAt': datetime.now().isoformat()
            }
        )
        
        # Add to vector store
        doc_ids = vector_store.add_documents([doc])
        doc_id = doc_ids[0] if doc_ids else None
        
        print(f"✓ Successfully loaded '{os.path.basename(file_path)}' ({len(content)} characters)")
        
        return doc_id
    
    except FileNotFoundError:
        print(f"❌ Error: File not found '{file_path}'")
        return None
    
    except Exception as e:
        print(f"❌ Error loading document '{file_path}': {str(e)}")
        return None

def main():
    print("🤖 Python LangChain Agent Starting...\n")

    # Check for GitHub token
    if not os.getenv("GITHUB_TOKEN"):
        print("❌ Error: GITHUB_TOKEN not found in environment variables.")
        print("Please create a .env file with your GitHub token:")
        print("GITHUB_TOKEN=your-github-token-here")
        print("\nGet your token from: https://github.com/settings/tokens")
        print("Or use GitHub Models: https://github.com/marketplace/models")
        return
    
    # Create OpenAI Embeddings instance
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
        check_embedding_ctx_length=False
    )
    
    # Create InMemoryVectorStore instance
    vector_store = InMemoryVectorStore(embeddings)
    
    # Load documents into vector database
    print("=== Loading Documents into Vector Database ===\n")
    
    # Load HealthInsuranceBrochure.md
    brochure_path = os.path.join(os.path.dirname(__file__), "HealthInsuranceBrochure.md")
    doc_id = load_document(vector_store, brochure_path)
    
    if doc_id:
        print(f"✓ Document successfully stored with ID: {doc_id}\n")
    
    return vector_store

if __name__ == "__main__":
    main()
