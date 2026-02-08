import os
import math
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

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
    
    print("=== Embedding Inspector Lab ===")
    print("Generating embeddings for three sentences...\n")
    
    # Test sentences
    test_sentences = [
        "The dog barked loudly.",
        "El perro ladró fuerte.",  # Spanish
        "Le chien a aboyé fort."  # French
    ]
    
    # Generate embeddings for each sentence
    sentence_embeddings = []
    for i, sentence in enumerate(test_sentences, 1):
        embedding = embeddings.embed_query(sentence)
        sentence_embeddings.append(embedding)
        print(f"Sentence {i}: \"{sentence}\"")
    
    # Calculate and display cosine similarities
    print("\n=== Cosine Similarities ===\n")
    
    similarity_1_2 = cosine_similarity(sentence_embeddings[0], sentence_embeddings[1])
    print(f"Cosine similarity between Sentence 1 and Sentence 2: {similarity_1_2:.4f}")
    
    similarity_2_3 = cosine_similarity(sentence_embeddings[1], sentence_embeddings[2])
    print(f"Cosine similarity between Sentence 2 and Sentence 3: {similarity_2_3:.4f}")
    
    similarity_3_1 = cosine_similarity(sentence_embeddings[2], sentence_embeddings[0])
    print(f"Cosine similarity between Sentence 3 and Sentence 1: {similarity_3_1:.4f}")

if __name__ == "__main__":
    main()
