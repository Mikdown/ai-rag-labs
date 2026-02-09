User: At the top of the application please do the following: Import InMemoryVectorStore from langchain_core.vectorstores at the top of app.py.
Also import datetime for timestamp metadata.

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#1-1), lines 1 to 30

Replacing 4 lines with 6 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```
Done! I've added both imports to the top of app.py:
- `import datetime` for timestamp metadata
- `from langchain_core.vectorstores import InMemoryVectorStore` from langchain_core

The imports are now organized at the top of the file after the existing imports.

Made changes.

User: After initializing the embeddings model in main(), create an InMemoryVectorStore instance:
- Create it with InMemoryVectorStore(embeddings) where embeddings is your OpenAIEmbeddings instance
- Store it in a variable called vector_store

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#23-23), lines 23 to 74

Replacing 9 lines with 12 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```
Done! I've added the InMemoryVectorStore initialization right after the embeddings model is created in main(). The vector_store is now instantiated with your OpenAIEmbeddings instance and ready to use.

Made changes.

User: Replace the current embedding generation code with the following logic:
1. Create the sentences list with 3 test sentences (same as Lab 1)
2. Use the vector_store.add_texts() method to add all sentences at once
3. Add metadata for each sentence including:
   - created_at: Current timestamp using datetime.now().isoformat()
   - index: The position in the original list
4. Print a confirmation message showing how many sentences were stored
5. Print each sentence that was added

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#32-32), lines 32 to 76

Replacing 28 lines with 26 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```
Done! I've replaced the embedding generation code with the new logic that:

1. Creates the test sentences list with 3 sentences
2. Generates metadata for each sentence with `created_at` (current timestamp) and `index`
3. Uses `vector_store.add_texts()` to add all sentences at once with their metadata
4. Prints a confirmation message showing 3 sentences were stored
5. Prints each sentence that was added in a numbered list format

The old cosine similarity code has been removed since the focus is now on storing sentences in the vector store with metadata.

Made changes.

User: Create a function called search_sentences that:
- Takes parameters: the vector_store and a search query string
- Optionally takes k (default to 3) for the number of results to return
- Uses vector_store.similarity_search_with_score() to find similar documents
- Returns the top k most similar results with their similarity scores
- Print the results with formatting showing:
  - Rank number (1, 2, 3...)
  - Similarity score formatted to 4 decimal places
  - The sentence text

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#1-1), lines 1 to 30

Replacing 3 lines with 24 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```
Done! I've created the `search_sentences` function with all the requested features:

- Takes `vector_store`, `query`, and optional `k` parameter (defaults to 3)
- Uses `vector_store.similarity_search_with_score()` to find similar documents
- Returns the results for further processing
- Prints formatted results showing:
  - Rank number (1, 2, 3...)
  - Similarity score to 4 decimal places
  - The sentence text

The function is positioned between `cosine_similarity` and `main()` for logical organization.

Made changes.

User: After storing the sentences, add an interactive loop that:
1. Display a header "=== Semantic Search ==="
2. Start a while True loop
3. Prompt the user to "Enter a search query (or 'quit' to exit): " using input()
4. If the user types "quit" or "exit", break the loop
5. If the input is empty or whitespace only, continue to the next iteration
6. Otherwise, call the search_sentences function with the user's query
7. Display the results
8. Print a blank line between searches for readability
9. After the loop ends, print a goodbye message

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#60-60), lines 60 to 98

Replacing 6 lines with 26 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```
Done! I've added an interactive semantic search loop that:

1. Displays the "=== Semantic Search ===" header
2. Enters a `while True` loop
3. Prompts users with "Enter a search query (or 'quit' to exit): "
4. Exits when user types "quit" or "exit"
5. Skips empty or whitespace-only queries
6. Calls the `search_sentences` function with valid queries
7. Prints blank lines between searches for readability
8. Displays a goodbye message when the loop exits

The loop is positioned right after the sentences are stored and printed, making it ready for immediate use.

Made changes.

User: please correct the following error: Traceback (most recent call last):
  File "c:\Users\mikdo\CodeYou\ai-rag-labs\app.py", line 117, in <module>
    main()
    ~~~~^^
  File "c:\Users\mikdo\CodeYou\ai-rag-labs\app.py", line 82, in main
    "created_at": datetime.now().isoformat(),
                  ^^^^^^^^^^^^
AttributeError: module 'datetime' has no attribute 'now'

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#1-1), lines 1 to 10

Replacing 6 lines with 6 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```
Fixed! The issue was that we imported the `datetime` module instead of the `datetime` class. I've changed the import to `from datetime import datetime` so that `datetime.now()` now correctly references the class method instead of trying to call `now()` on the module.

Made changes.

User: please correct the following errors: Enter a search query (or 'quit' to exit): The quick brown fox jumpped over the lazy 
dog.
Traceback (most recent call last):
  File "c:\Users\mikdo\CodeYou\ai-rag-labs\app.py", line 117, in <module>
    main()
    ~~~~^^
  File "c:\Users\mikdo\CodeYou\ai-rag-labs\app.py", line 111, in main
    search_sentences(vector_store, user_query)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\mikdo\CodeYou\ai-rag-labs\app.py", line 37, in search_sentences    
    results = vector_store.similarity_search_with_score(query, k=k)
  File "c:\Users\mikdo\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\langchain_core\vectorstores\in_memory.py", line 366, in similarity_search_with_score   
    return self.similarity_search_with_score_by_vector(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        embedding,
        ^^^^^^^^^^
        k,
        ^^
        **kwargs,
        ^^^^^^^^^
    )
    ^
  File "c:\Users\mikdo\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\langchain_core\vectorstores\in_memory.py", line 353, in similarity_search_with_score_by_vector
    for doc, similarity, _ in self._similarity_search_with_score_by_vector(
                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        embedding=embedding, k=k, filter=filter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "c:\Users\mikdo\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\langchain_core\vectorstores\in_memory.py", line 314, in _similarity_search_with_score_by_vector
    similarity = cosine_similarity([embedding], [doc["vector"] for doc in docs])[0] 
                 ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "c:\Users\mikdo\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\langchain_core\vectorstores\utils.py", line 55, in _cosine_similarity
    raise ImportError(msg)
ImportError: cosine_similarity requires numpy to be installed. Please install numpy with `pip install numpy`.

GitHub Copilot: Ran terminal command: pip install numpy

Configuring a Python Environment
Completed with input: {
  "resourcePath": "c:\\Users\\mikdo\\CodeYou\\ai-rag-labs"
}

Creating a Virtual Environment
Completed with input: {
  "resourcePath": "c:\\Users\\mikdo\\CodeYou\\ai-rag-labs"
}

User: please resolve the following errors: Enter a search query (or 'quit' to exit): The quick brown fox
Traceback (most recent call last):
  File "c:\Users\mikdo\CodeYou\ai-rag-labs\app.py", line 117, in <module>
    main()
    ~~~~^^
  File "c:\Users\mikdo\CodeYou\ai-rag-labs\app.py", line 111, in main
    search_sentences(vector_store, user_query)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\mikdo\CodeYou\ai-rag-labs\app.py", line 37, in search_sentences    
    results = vector_store.similarity_search_with_score(query, k=k)
  File "c:\Users\mikdo\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\langchain_core\vectorstores\in_memory.py", line 366, in similarity_search_with_score   
    return self.similarity_search_with_score_by_vector(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        embedding,
        ^^^^^^^^^^
        k,
        ^^
        **kwargs,
        ^^^^^^^^^
    )
    ^
  File "c:\Users\mikdo\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\langchain_core\vectorstores\in_memory.py", line 353, in similarity_search_with_score_by_vector
    for doc, similarity, _ in self._similarity_search_with_score_by_vector(
                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        embedding=embedding, k=k, filter=filter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "c:\Users\mikdo\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\langchain_core\vectorstores\in_memory.py", line 314, in _similarity_search_with_score_by_vector
    similarity = cosine_similarity([embedding], [doc["vector"] for doc in docs])[0] 
                 ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "c:\Users\mikdo\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\langchain_core\vectorstores\utils.py", line 55, in _cosine_similarity
    raise ImportError(msg)
ImportError: cosine_similarity requires numpy to be installed. Please install numpy with `pip install numpy`.

GitHub Copilot: Installing numpy in Python 3.14.2
Completed with input: {
  "packageList": [
    "numpy"
  ],
  "resourcePath": "c:\\Users\\mikdo\\CodeYou\\ai-rag-labs"
}

Done! I've installed numpy, which is required by InMemoryVectorStore for similarity calculations. Your search should now work without the ImportError.

User: pleasde add each of the following sentences to test_sentences:  "The canine barked loudly.",
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

GitHub Copilot: Read [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py#70-70), lines 70 to 90

Replacing 4 lines with 21 lines in [](file:///c%3A/Users/mikdo/CodeYou/ai-rag-labs/app.py)


```

```
Done! I've updated the `test_sentences` list to include all 18 sentences - the original 3 plus the 15 new ones you provided. The vector store will now have more diverse content to search across, including sentences about movies, animals, physics, food, sports, technology, and more.

Made changes.