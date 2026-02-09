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
    
    # Test sentences
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
    
    # Create metadata for each sentence
    metadatas = [
        {
            "created_at": datetime.now().isoformat(),
            "index": i
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
    print("\n=== Semantic Search ===\n")
    
    while True:
        user_query = input("Enter a search query (or 'quit' to exit): ").strip()
        
        # Check if user wants to exit
        if user_query.lower() in ['quit', 'exit']:
            break
        
        # Skip empty queries
        if not user_query:
            continue
        
        # Perform search
        search_sentences(vector_store, user_query)
        print()  # Blank line for readability
    
    print("\n👋 Thank you for using the Semantic Search tool. Goodbye!")

if __name__ == "__main__":
    main()
