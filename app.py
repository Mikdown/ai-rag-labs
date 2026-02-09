import os
import math
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

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
    
    print("=== Embedding Inspector Lab ===")
    print("Adding sentences to vector store...\n")
    
    # Test sentences with categories
    test_sentences = [
        "The movie F1 was excellent and entertaining.",
        "I enjoyed watching the film Castaway.",
        "The canine barked loudly.",
        "The dog made a noise.",
        "The electron spins rapidly.",
        "I love eating pizza with extra cheese.",
        "The basketball player scored a three-pointer.",
        "Rain is forecasted for tomorrow afternoon.",
        "Python is a popular programming language.",
        "The kitten purred softly on the couch.",
        "Quantum mechanics explains particle behavior.",
        "Homemade pasta tastes better than store-bought.",
        "The soccer match ended in a tie.",
        "Clouds are forming over the mountains.",
        "JavaScript runs in web browsers.",
        "Puppies need lots of attention and exercise.",
        "Atoms are made of protons, neutrons, and electrons."
    ]
    
    # Define categories for each sentence
    categories = [
        "movies",
        "movies",
        "animals",
        "animals",
        "science",
        "food",
        "sports",
        "weather",
        "programming",
        "animals",
        "science",
        "food",
        "sports",
        "weather",
        "programming",
        "animals",
        "science"
    ]
    
    # Create metadata for each sentence including category
    metadatas = [
        {
            "created_at": datetime.now().isoformat(),
            "index": i,
            "category": categories[i]
        }
        for i in range(len(test_sentences))
    ]
    
    # Add all sentences to vector store at once
    vector_store.add_texts(test_sentences, metadatas=metadatas)
    
    print(f"✓ Successfully stored {len(test_sentences)} sentences in vector store\n")
    print("Sentences added:")
    for i, sentence in enumerate(test_sentences, 1):
        print(f"  {i}. \"{sentence}\"")
    
    # Interactive semantic search loop
    print("\n=== Semantic Search ===")
    print("Available Categories:", ", ".join(get_available_categories(vector_store)))
    print("\nCommands:")
    print("  - 'vector <query>' or just '<query>' for vector similarity search")
    print("  - 'hybrid <query>' for hybrid search (vector + keyword matching)")
    print("  - 'both <query>' to compare both methods")
    print("  - 'categories' to list available categories")
    print("  - 'vector-cat <category> <query>' for category-filtered vector search")
    print("  - 'hybrid-cat <category> <query>' for category-filtered hybrid search")
    print("  - 'quit' or 'exit' to close\n")
    
    while True:
        user_input = input("Enter search command: ").strip()
        
        # Check if user wants to exit
        if user_input.lower() in ['quit', 'exit']:
            break
        
        # Skip empty input
        if not user_input:
            continue
        
        # Handle special commands
        if user_input.lower() == 'categories':
            categories = get_available_categories(vector_store)
            print(f"\n✓ Available Categories ({len(categories)}):")
            for i, cat in enumerate(categories, 1):
                print(f"  {i}. {cat}")
            print()
            continue
        
        # Parse command and query
        parts = user_input.split(maxsplit=2)
        command = parts[0].lower() if parts else 'vector'
        
        # Handle category-filtered searches
        if command in ['vector-cat', 'hybrid-cat']:
            if len(parts) < 3:
                print("❌ Usage: 'vector-cat <category> <query>' or 'hybrid-cat <category> <query>'\n")
                continue
            
            category = parts[1].lower()
            query = parts[2]
            
            # Check if category exists
            available_categories = get_available_categories(vector_store)
            if category not in available_categories:
                print(f"❌ Category '{category}' not found. Available: {', '.join(available_categories)}\n")
                continue
            
            if command == 'vector-cat':
                search_by_category(vector_store, query, category)
            else:  # hybrid-cat
                hybrid_search_by_category(vector_store, query, category)
            print()
            continue
        
        # Handle regular searches
        query = parts[1] if len(parts) > 1 else (parts[0] if len(parts) == 1 and command not in ['vector', 'hybrid', 'both'] else '')
        
        # Handle different commands
        if command in ['vector', 'hybrid', 'both'] and query:
            if command in ['vector', 'both']:
                search_sentences(vector_store, query)
            if command in ['hybrid', 'both']:
                if command == 'both':
                    print()  # Add spacing between methods
                hybrid_search(vector_store, query)
        elif command not in ['vector', 'hybrid', 'both']:
            # No command prefix, treat entire input as query for vector search
            search_sentences(vector_store, user_input)
        else:
            print("❌ Please enter a valid query. Use 'help' for commands or type 'quit' to exit.\n")
            continue
        
        print()  # Blank line for readability
    
    print("\n👋 Thank you for using the Semantic Search tool. Goodbye!")

if __name__ == "__main__":
    main()
