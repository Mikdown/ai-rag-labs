import os
import math
from datetime import datetime
from dotenv import load_dotenv
import tiktoken
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

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
        
        # Calculate token count
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        token_count = len(encoding.encode(content))
        
        # Add to vector store
        doc_ids = vector_store.add_documents([doc])
        doc_id = doc_ids[0] if doc_ids else None
        
        print(f"✓ Successfully loaded '{os.path.basename(file_path)}' ({len(content)} characters, {token_count} tokens)")
        
        return doc_id
    
    except FileNotFoundError:
        print(f"❌ Error: File not found '{file_path}'")
        return None
    
    except Exception as e:
        print(f"❌ Error loading document '{file_path}': {str(e)}")
        return None

def load_document_with_chunks(vector_store, file_path, chunks):
    """
    Load document chunks into the vector store with enhanced metadata.
    
    Args:
        vector_store: The InMemoryVectorStore instance
        file_path: Path to the original document file
        chunks: List of LangChain Document objects (chunks)
    
    Returns:
        Total number of chunks stored
    
    Raises:
        Exception: For processing errors during chunk loading
    """
    try:
        if not chunks:
            print(f"⚠️  Warning: No chunks provided for '{os.path.basename(file_path)}'")
            return 0
        
        file_name = os.path.basename(file_path)
        total_chunks = len(chunks)
        
        print(f"📦 Loading {total_chunks} chunks from '{file_name}'...\n")
        
        for idx, chunk in enumerate(chunks, 1):
            # Update chunk metadata
            chunk.metadata.update({
                'fileName': f"{file_name} (Chunk {idx}/{total_chunks})",
                'createdAt': datetime.now().isoformat(),
                'chunkIndex': idx
            })
            
            # Add chunk to vector store
            try:
                vector_store.add_documents([chunk])
                print(f"   ✓ Chunk {idx}/{total_chunks} processed ({len(chunk.page_content)} characters)")
            except Exception as e:
                print(f"   ❌ Error processing chunk {idx}/{total_chunks}: {str(e)}")
                continue
        
        print(f"\n✓ Successfully loaded all {total_chunks} chunks from '{file_name}'\n")
        return total_chunks
    
    except Exception as e:
        print(f"❌ Error loading chunks from '{file_path}': {str(e)}")
        return 0

def load_with_fixed_size_chunking(vector_store, file_path):
    """
    Load a document and split it into fixed-size chunks using CharacterTextSplitter.
    
    Args:
        vector_store: The InMemoryVectorStore instance
        file_path: Path to the document file to load
    
    Returns:
        Number of chunks created and added to the vector store
    
    Raises:
        FileNotFoundError: If the file does not exist
        Exception: For other I/O or processing errors
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if not text:
            print(f"⚠️  Warning: File '{os.path.basename(file_path)}' is empty")
            return 0
        
        # Create CharacterTextSplitter instance
        splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
            separator=" "
        )
        
        # Create Document objects from chunks
        chunks = splitter.create_documents([text])
        
        if not chunks:
            print(f"⚠️  Warning: No chunks created from '{os.path.basename(file_path)}'")
            return 0
        
        # Calculate statistics
        num_chunks = len(chunks)
        total_chars = sum(len(chunk.page_content) for chunk in chunks)
        avg_chunk_size = total_chars / num_chunks if num_chunks > 0 else 0
        
        print(f"📊 Chunking Statistics for '{os.path.basename(file_path)}':")
        print(f"   - Number of chunks: {num_chunks}")
        print(f"   - Average chunk size: {avg_chunk_size:.0f} characters")
        print(f"   - Total content size: {total_chars} characters\n")
        
        # Load chunks into vector store
        chunks_stored = load_document_with_chunks(vector_store, file_path, chunks)
        
        return chunks_stored
    
    except FileNotFoundError:
        print(f"❌ Error: File not found '{file_path}'")
        return 0
    
    except Exception as e:
        print(f"❌ Error processing document '{file_path}': {str(e)}")
        return 0

def load_with_paragraph_chunking(vector_store, file_path):
    """
    Load a document and split it by paragraphs using RecursiveCharacterTextSplitter.
    This preserves paragraph structure while respecting size limits.
    
    Args:
        vector_store: The InMemoryVectorStore instance
        file_path: Path to the document file to load
    
    Returns:
        Number of chunks created and added to the vector store
    
    Raises:
        FileNotFoundError: If the file does not exist
        Exception: For other I/O or processing errors
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if not text:
            print(f"⚠️  Warning: File '{os.path.basename(file_path)}' is empty")
            return 0
        
        # Create RecursiveCharacterTextSplitter instance
        # This splits on paragraphs first (\n\n), then lines (\n), then spaces, then characters
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=0,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Create Document objects from chunks
        chunks = splitter.create_documents([text])
        
        if not chunks:
            print(f"⚠️  Warning: No chunks created from '{os.path.basename(file_path)}'")
            return 0
        
        # Calculate statistics
        num_chunks = len(chunks)
        chunk_sizes = [len(chunk.page_content) for chunk in chunks]
        total_chars = sum(chunk_sizes)
        avg_chunk_size = total_chars / num_chunks if num_chunks > 0 else 0
        min_chunk_size = min(chunk_sizes)
        max_chunk_size = max(chunk_sizes)
        
        # Count chunks starting with newline (paragraph preservation indicator)
        newline_start_count = sum(1 for chunk in chunks if chunk.page_content.startswith("\n"))
        
        print(f"📊 Paragraph-Based Chunking Statistics for '{os.path.basename(file_path)}':")
        print(f"   - Number of chunks: {num_chunks}")
        print(f"   - Average chunk size: {avg_chunk_size:.0f} characters")
        print(f"   - Smallest chunk: {min_chunk_size} characters")
        print(f"   - Largest chunk: {max_chunk_size} characters")
        print(f"   - Chunks preserving paragraphs: {newline_start_count} (start with newline)")
        print(f"   - Total content size: {total_chars} characters\n")
        
        # Load chunks into vector store
        chunks_stored = load_document_with_chunks(vector_store, file_path, chunks)
        
        return chunks_stored
    
    except FileNotFoundError:
        print(f"❌ Error: File not found '{file_path}'")
        return 0
    
    except Exception as e:
        print(f"❌ Error processing document '{file_path}': {str(e)}")
        return 0

def load_with_markdown_structure_chunking(vector_store, file_path):
    """
    Load a markdown document and split it by structure (headers) then by size.
    First splits on markdown headers, then applies recursive character splitting.
    This preserves document structure and context across chunk boundaries.
    
    Args:
        vector_store: The InMemoryVectorStore instance
        file_path: Path to the markdown document file to load
    
    Returns:
        Number of chunks created and added to the vector store
    
    Raises:
        FileNotFoundError: If the file does not exist
        Exception: For other I/O or processing errors
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if not text:
            print(f"⚠️  Warning: File '{os.path.basename(file_path)}' is empty")
            return 0
        
        # Define markdown headers to split on
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2")
        ]
        
        # Create MarkdownHeaderTextSplitter instance
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        
        # Split on markdown headers
        markdown_chunks = markdown_splitter.split_text(text)
        
        if not markdown_chunks:
            print(f"⚠️  Warning: No chunks created from markdown headers in '{os.path.basename(file_path)}'")
            return 0
        
        # Apply recursive character splitting for size management
        recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=5000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Further split markdown chunks if needed
        final_chunks = []
        for chunk in markdown_chunks:
            # Recursive splitter expects Document or string list
            sub_chunks = recursive_splitter.split_documents([chunk])
            final_chunks.extend(sub_chunks)
        
        if not final_chunks:
            print(f"⚠️  Warning: No final chunks created from '{os.path.basename(file_path)}'")
            return 0
        
        # Calculate statistics
        num_chunks = len(final_chunks)
        chunk_sizes = [len(chunk.page_content) for chunk in final_chunks]
        total_chars = sum(chunk_sizes)
        avg_chunk_size = total_chars / num_chunks if num_chunks > 0 else 0
        min_chunk_size = min(chunk_sizes)
        max_chunk_size = max(chunk_sizes)
        
        # Count chunks with header metadata
        chunks_with_headers = sum(1 for chunk in final_chunks if chunk.metadata and ("Header 1" in chunk.metadata or "Header 2" in chunk.metadata))
        
        print(f"📑 Markdown Structure-Based Chunking Statistics for '{os.path.basename(file_path)}':")
        print(f"   - Number of chunks: {num_chunks}")
        print(f"   - Average chunk size: {avg_chunk_size:.0f} characters")
        print(f"   - Smallest chunk: {min_chunk_size} characters")
        print(f"   - Largest chunk: {max_chunk_size} characters")
        print(f"   - Chunk overlap: 200 characters")
        print(f"   - Chunks with header metadata: {chunks_with_headers}")
        print(f"   - Total content size: {total_chars} characters\n")
        
        # Load chunks into vector store
        chunks_stored = load_document_with_chunks(vector_store, file_path, final_chunks)
        
        return chunks_stored
    
    except FileNotFoundError:
        print(f"❌ Error: File not found '{file_path}'")
        return 0
    
    except Exception as e:
        print(f"❌ Error processing document '{file_path}': {str(e)}")
        return 0

def create_search_tool(vector_store):
    """
    Create a search tool that agents can use to query the document repository.
    
    Args:
        vector_store: The InMemoryVectorStore instance containing documents
    
    Returns:
        A LangChain Tool that can search the vector store
    """
    @tool
    def search_documents(query: str) -> str:
        """
        Searches the company document repository for relevant information based on the given query.
        Use this to find information about company policies, benefits, and procedures.
        
        Args:
            query: The search query string
        
        Returns:
            Formatted search results with similarity scores
        """
        try:
            # Search for top 3 similar documents
            results = vector_store.similarity_search_with_score(query, k=3)
            
            if not results:
                return "No relevant documents found for your query."
            
            # Format results as a readable string
            formatted_results = []
            for idx, (document, score) in enumerate(results, 1):
                formatted_results.append(
                    f"Result {idx} (Score: {score:.4f}): {document.page_content}"
                )
            
            return "\n\n".join(formatted_results)
        
        except Exception as e:
            return f"Error searching documents: {str(e)}"
    
    return search_documents

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
    
    # Create ChatOpenAI model instance
    chat_model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN")
    )
    
    # Load documents into vector database
    print("=== Loading Documents into Vector Database ===\n")
    
    # Load HealthInsuranceBrochure.md
    brochure_path = os.path.join(os.path.dirname(__file__), "HealthInsuranceBrochure.md")
    doc_id = load_document(vector_store, brochure_path)
    
    if doc_id:
        print(f"✓ Document successfully stored with ID: {doc_id}\n")
    
    # Load EmployeeHandbook.md with markdown structure-based chunking
    handbook_path = os.path.join(os.path.dirname(__file__), "EmployeeHandbook.md")
    chunks_stored = load_with_markdown_structure_chunking(vector_store, handbook_path)
    
    if chunks_stored:
        print(f"✓ Successfully stored {chunks_stored} chunks from EmployeeHandbook\n")
    
    # Create the search tool
    print("=== Setting Up ReAct Agent ===\n")
    search_tool = create_search_tool(vector_store)
    
    # Create the prompt template for the agent
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful assistant that answers questions about company policies, benefits, and procedures. "
            "Always search for relevant information using search_documents before answering. "
            "Always cite which documents you used in your answer."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    
    # Create an agent that can use the search tool
    tools = [search_tool]
    model_with_tools = chat_model.bind_tools(tools)
    
    # Create a function to process tool calls
    def process_tool_call(tool_name, tool_input):
        """Execute a tool call and return the result"""
        if tool_name == "search_documents":
            return search_tool(tool_input.get("query", ""))
        return "Tool not found"
    
    print("✓ Agent successfully initialized\n")
    
    # Initialize chat history for multi-turn conversations
    chat_history = []
    
    # Welcome message
    print("=" * 60)
    print("🤖 Company Document Assistant")
    print("=" * 60)
    print("Welcome! I'm an AI assistant trained on company policies, benefits, and procedures.")
    print("I can help answer your questions about:")
    print("  • Employee benefits and insurance")
    print("  • Company policies and procedures")
    print("  • HR guidelines and requirements")
    print("\nType 'quit' or 'exit' to end the conversation.")
    print("=" * 60 + "\n")
    
    # Chat loop
    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Exit on quit/exit
            if user_input.lower() in ["quit", "exit"]:
                print("\nAgent: Thank you for using the Company Document Assistant. Goodbye!")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Invoke the agent
            try:
                # Format the prompt with the current input and chat history
                formatted_prompt = prompt.invoke({
                    "input": user_input,
                    "chat_history": chat_history
                })
                
                # Invoke the model with tools using the formatted prompt
                response = model_with_tools.invoke(formatted_prompt)
                
                # Check if the model wants to call a tool
                tool_calls = getattr(response, 'tool_calls', [])
                
                if tool_calls:
                    # Execute the tool call
                    tool_call = tool_calls[0]
                    tool_name = tool_call.get('name', tool_call.name if hasattr(tool_call, 'name') else '')
                    tool_args = tool_call.get('args', tool_call.args if hasattr(tool_call, 'args') else {})
                    
                    # Call the search tool using invoke method
                    search_query = tool_args.get('query', user_input) if isinstance(tool_args, dict) else user_input
                    tool_result = search_tool.invoke({"query": search_query})
                    
                    # Create a new message with the tool result and get final response
                    tool_message = f"Search results for '{search_query}':\n{tool_result}"
                    
                    # Get the final response from the model using the tool results
                    final_messages = chat_history + [
                        HumanMessage(content=user_input),
                        response,
                        {"role": "tool", "content": tool_result, "tool_call_id": tool_call.get('id', '0')}
                    ]
                    
                    # Ask model to formulate final answer
                    final_response = chat_model.invoke([
                        {"role": "system", "content": "You are a helpful assistant answering questions about company policies. Use the search results provided to give a detailed answer."},
                        *final_messages
                    ])
                    agent_response = final_response.content if hasattr(final_response, 'content') else str(final_response)
                else:
                    # If no tool call, use the response directly
                    agent_response = response.content if hasattr(response, 'content') else str(response)
                
                # Ensure we have a non-empty response
                if not agent_response or agent_response.strip() == "":
                    # Fallback: search and provide results directly
                    search_results = search_tool.invoke({"query": user_input})
                    agent_response = f"Based on the company documents: {search_results}"
                
                print(f"\nAgent: {agent_response}\n")
                
                # Add to chat history
                chat_history.append(HumanMessage(content=user_input))
                chat_history.append(AIMessage(content=agent_response))
            
            except Exception as e:
                print(f"\n⚠️  Error processing request: {str(e)}\n")
                import traceback
                traceback.print_exc()
                continue
    
    except KeyboardInterrupt:
        print("\n\nAgent: Conversation interrupted. Goodbye!")
    
    return vector_store, chat_model, model_with_tools

if __name__ == "__main__":
    main()
