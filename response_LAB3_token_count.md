User: I need to understand how to store documents in the InMemoryVectorStore.
Each document will have:
- page_content: the document text
- metadata: a dictionary with 'fileName', 'createdAt', and any other relevant fields
- The embedding is generated automatically by the vector store

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#1-1), lines 1 to 100

Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#100-100), lines 100 to 200

Let me read the rest of the file to see how documents are currently being added: 

Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#200-200), lines 200 to 363

Based on your code, here's how to store documents in the `InMemoryVectorStore`:

## Basic Setup

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

# Create embeddings instance
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

# Create vector store
vector_store = InMemoryVectorStore(embeddings)
```

## Storing Documents

```python
from datetime import datetime

# Prepare your documents
documents = [
    "The movie F1 was excellent and entertaining.",
    "I enjoyed watching the film Castaway.",
    "Python is a popular programming language."
]

# Prepare metadata for each document
metadatas = [
    {
        "fileName": "doc1.txt",
        "createdAt": datetime.now().isoformat(),
        "category": "movies"
    },
    {
        "fileName": "doc2.txt",
        "createdAt": datetime.now().isoformat(),
        "category": "movies"
    },
    {
        "fileName": "doc3.txt",
        "createdAt": datetime.now().isoformat(),
        "category": "programming"
    }
]

# Store documents - embeddings are generated automatically
vector_store.add_texts(documents, metadatas=metadatas)
```

## Key Points

- **`page_content`**: Passed as the `texts` parameter to `add_texts()` 
- **`metadata`**: Each dict in the `metadatas` list stores your custom fields (`fileName`, `createdAt`, etc.)
- **Embeddings**: Generated automatically by the `embeddings` object when you call `add_texts()`
- **Access**: Metadata is accessible in search results via `document.metadata` on returned Document objects

Your current code already demonstrates this pattern at lines 260-280 where you add the test sentences with categories.

User: Remove all the code that:
- Creates the sentences list
- Adds sentences to the vector store using add_texts()
- The search loop from Lab 2

Keep the vector store initialization code (InMemoryVectorStore), but we'll be adding different data loading logic.

GitHub Copilot: Replacing 145 lines with 4 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```


Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#195-195), lines 195 to 222

Done! I've removed:
- The test_sentences list
- The categories list
- The metadatas creation
- The `add_texts()` call and related print statements
- The entire interactive search loop

The app.py now keeps the vector store initialization and returns it from `main()`, so you can use it to load different data. The helper functions (`search_sentences()`, `hybrid_search()`, etc.) remain available for use with your new data loading logic.

Made changes.

User: Create a function called load_document that:
- Takes parameters: the vector_store and a file_path (string)
- Reads all text from the file using open() and read()
- Creates a LangChain Document object with:
  - page_content: The full document text
  - metadata: A dictionary with:
    - 'fileName': The file name from the path (use os.path.basename(file_path))
    - 'createdAt': Current timestamp using datetime.now().isoformat()
- Adds the document to the vector store using vector_store.add_documents([document])
- Prints a success message with the filename and content length
- Returns the document ID

Add error handling using try-except for FileNotFoundError and other exceptions.
Import Document from langchain_core.documents

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#1-1), lines 1 to 10

Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#185-185), lines 185 to 195

Replacing 9 lines with 58 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```


Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#1-1), lines 1 to 20

Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#190-190), lines 190 to 245

Done! I've added the `load_document` function with:

✅ **Import**: Added `Document` from `langchain_core.documents`

✅ **Function Features**:
- Takes `vector_store` and `file_path` parameters
- Reads file content using `open()` with UTF-8 encoding
- Creates a `Document` object with:
  - `page_content`: The full file text
  - `metadata`: Dictionary with `fileName` and `createdAt` fields
- Adds to vector store using `add_documents()`
- Returns the document ID (first ID from the response, or None on error)
- Includes success message with filename and content length
- Empty file warning
- Comprehensive error handling for `FileNotFoundError` and other exceptions

The function is now ready to use for loading documents into your vector store!

Made changes.

User: After the vector store is created, call the load_document function to load the file "HealthInsuranceBrochure.md" from the workspace root directory.
Display a header "=== Loading Documents into Vector Database ===" before loading.
Print the filename and a confirmation when it loads successfully.

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#245-245), lines 245 to 271

Replacing 4 lines with 14 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```


Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#255-255), lines 255 to 280

Done! I've updated the app.py to:

1. **Added header** before loading: `"=== Loading Documents into Vector Database ==="`
2. **Constructed the file path** to `HealthInsuranceBrochure.md` in the workspace root using `os.path.join()` and `os.path.dirname(__file__)`
3. **Called `load_document()`** which will display:
   - The filename
   - Content size (character count)
   - Success confirmation
4. **Added document ID confirmation** showing the returned document ID after successful load

When you run the app, you'll see output like:
```
=== Loading Documents into Vector Database ===

✓ Successfully loaded 'HealthInsuranceBrochure.md' (XXXX characters)
✓ Document successfully stored with ID: <id>
```

Made changes.

User: After loading the HealthInsuranceBrochure.md, add another call to load_document to load "EmployeeHandbook.md" from the workspace root directory.

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#265-265), lines 265 to 276

Replacing 9 lines with 16 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```
Done! I've added a call to load EmployeeHandbook.md right after the HealthInsuranceBrochure.md is loaded. Both documents will now be added to the vector store in sequence.

Made changes.

User: please add the code to return the token count along with the character count

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#1-1), lines 1 to 10

Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#196-196), lines 196 to 240

Replacing 14 lines with 19 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```


Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#1-1), lines 1 to 15

Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#225-225), lines 225 to 245

Done! I've added token counting to the `load_document` function:

✅ **Added `tiktoken` import** at the top
✅ **Added token calculation** using the gpt-3.5-turbo tokenizer before adding to the vector store
✅ **Updated success message** to display both character count and token count

Now when documents load, you'll see output like:
```
✓ Successfully loaded 'HealthInsuranceBrochure.md' (15234 characters, 3892 tokens)
```

Made changes.