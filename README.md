# Agentic AI RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built using Python, LangGraph, Pinecone, Hugging Face Sentence Transformers, Groq, and FastAPI.

The chatbot uses the provided **Agentic AI eBook** as its knowledge source and is designed to answer questions using retrieved information from the document.

---

## 1. Project Objective

The objective of this project is to build a RAG-based AI chatbot that can:

- Load and process the Agentic AI eBook
- Split the document into smaller text chunks
- Convert document chunks into vector embeddings
- Store the embeddings in Pinecone
- Retrieve relevant document chunks for a user question
- Use LangGraph to orchestrate the RAG workflow
- Generate answers using only the retrieved document context
- Refuse questions when the required information is not available in the document
- Expose the chatbot through a FastAPI REST API
- Return the final answer, retrieved context, and confidence score

The original assignment reference specifies OpenAI embeddings and an OpenAI LLM. During development, OpenAI API credits were unavailable, so this implementation uses a free/local embedding model and Groq for LLM inference.

The RAG architecture, Pinecone vector storage, LangGraph workflow, strict grounding approach, FastAPI interface, and benchmark testing remain aligned with the assignment objectives.

---

## 2. Architecture

The application follows this workflow:

```text
                  Agentic AI eBook
                         |
                         v
                   PDF Loader
                         |
                         v
                Text Chunking
              chunk_size = 1000
              overlap = 200
                         |
                         v
       Sentence Transformers Embeddings
       all-MiniLM-L6-v2 (384 dimensions)
                         |
                         v
                      Pinecone
                  Vector Database
                         |
                         v
                    User Query
                         |
                         v
                   LangGraph
                         |
             +-----------+-----------+
             |                       |
             v                       v
          Retrieve                Generate
             |                       |
             |                 Groq LLM
             |              openai/gpt-oss-20b
             |                       |
             +-----------+-----------+
                         |
                         v
                  Final Response
                         |
                         v
                      FastAPI
```

---

## 3. Technology Stack

### Programming Language

- Python 3.10+

### Frameworks and Libraries

- LangChain
- LangGraph
- LangChain Hugging Face
- LangChain Groq
- LangChain Pinecone
- Sentence Transformers
- PyPDF
- FastAPI
- Uvicorn
- Python Dotenv

### External Services

- Pinecone for vector storage
- Groq for LLM inference

### Local Model

Embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Embedding dimension:

```text
384
```

### LLM

Groq model:

```text
openai/gpt-oss-20b
```

---

## 4. Project Structure

```text
Assignment/
│
├── data/
│   └── Ebook-Agentic-AI.pdf
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   └── graph.py
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
└── tests_sample_queries.py
```

### File Description

#### `data/Ebook-Agentic-AI.pdf`

The Agentic AI eBook used as the knowledge source.

#### `src/config.py`

Loads environment variables from `.env`.

#### `src/ingestion.py`

Handles:

- PDF loading
- Text splitting
- Local embedding generation
- Pinecone vector storage

#### `src/graph.py`

Defines the LangGraph RAG workflow.

It contains:

- Agent state
- Retrieval node
- Generation node
- LangGraph workflow

#### `app.py`

FastAPI application containing the `/chat` endpoint.

#### `tests_sample_queries.py`

Contains benchmark questions used to test the chatbot.

---

## 5. Environment Setup

### Requirements

- Python 3.10 or higher
- 8 GB RAM recommended
- Pinecone account
- Groq API key

OpenAI API credentials are not required for the current implementation because embeddings are generated locally and Groq is used for LLM generation.

---

## 6. Clone the Repository

```bash
git clone https://github.com/blackeagle-25-5/Assignment.git
cd Assignment
```

---

## 7. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

You should see:

```text
(venv)
```

in your terminal.

---

## 8. Install Dependencies

Run:

```powershell
pip install -r requirements.txt
```

The main packages include:

```text
langchain
langgraph
langchain-huggingface
langchain-groq
langchain-pinecone
sentence-transformers
pinecone-client
pypdf
fastapi
uvicorn
python-dotenv
```

---

## 9. Environment Variables

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-index
GROQ_API_KEY=your_groq_api_key
```

### Security

Never commit the real `.env` file to GitHub.

The project `.gitignore` contains:

```text
venv/
.env
__pycache__/
*.pyc
```

A `.env.example` file is included for reference.

---

## 10. Pinecone Configuration

Create a Pinecone index using the following configuration:

```text
Index Name: agentic-ai-index
Vector Type: Dense
Dimension: 384
Metric: cosine
Cloud: AWS
Region: us-east-1
```

The dimension is 384 because the selected local embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

produces 384-dimensional vectors.

The same embedding model must be used during both:

1. Document ingestion
2. User-query retrieval

---

## 11. Document Ingestion

The ingestion pipeline performs the following steps:

```text
PDF
 ↓
PyPDFLoader
 ↓
Document pages
 ↓
RecursiveCharacterTextSplitter
 ↓
Text chunks
 ↓
Sentence Transformer embeddings
 ↓
Pinecone
```

The configured chunking parameters are:

```python
chunk_size=1000
chunk_overlap=200
```

Run ingestion with:

```powershell
python -m src.ingestion
```

A successful ingestion prints:

```text
Document ingestion completed successfully.
```

The provided eBook was successfully loaded and split into document chunks during development.

---

## 12. Embedding Model

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model runs locally through Sentence Transformers.

This avoids requiring paid OpenAI embedding API usage.

The embedding vector size is:

```text
384
```

Therefore the Pinecone index also uses:

```text
dimension = 384
```

---

## 13. RAG Workflow

The application uses LangGraph to organize the RAG pipeline.

The workflow is:

```text
START
  |
  v
retrieve
  |
  v
generate
  |
  v
END
```

### Retrieve Node

The retrieve node:

1. Receives the user question
2. Searches Pinecone
3. Retrieves the top 3 relevant document chunks
4. Stores the retrieved text in the graph state

The retriever is configured with:

```python
search_kwargs={"k": 3}
```

### Generate Node

The generate node:

1. Receives the user question
2. Receives retrieved document context
3. Sends the context and question to the Groq LLM
4. Instructs the model to use only the retrieved context
5. Returns the final answer
6. Returns a confidence score

---

## 14. Strict Grounding

The chatbot is instructed not to use outside knowledge.

The generation prompt contains rules such as:

```text
Use the retrieved context as the source of truth.

If the context genuinely does not contain enough
information to answer the question, respond:

"I cannot answer based on the provided document."

Do not use outside knowledge.
Do not invent or assume facts.
```

This is important because the chatbot should answer questions based on the Agentic AI eBook rather than behaving as a general-purpose chatbot.

---

## 15. FastAPI

The application exposes a REST API using FastAPI.

Start the server:

```powershell
uvicorn app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

The API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 16. Health Check

Open:

```text
http://127.0.0.1:8000
```

Expected response:

```json
{
  "message": "Agentic AI RAG API is running"
}
```

---

## 17. Chat Endpoint

Endpoint:

```text
POST /chat
```

Request:

```json
{
  "query": "What role does memory play in Agentic AI workflows?"
}
```

Example response:

```json
{
  "final_answer": "Memory in Agentic AI workflows serves several key functions...",
  "retrieved_context": [
    "Relevant eBook chunk...",
    "Another relevant eBook chunk..."
  ],
  "confidence_score": 0.95
}
```

The response contains:

### `final_answer`

The generated answer.

### `retrieved_context`

The document chunks retrieved from Pinecone.

### `confidence_score`

The confidence value generated by the current implementation based on retrieval availability.

---

## 18. Testing

The project includes benchmark questions based on the assignment.

### Test 1

```text
What is Agentic AI according to the eBook?
```

### Test 2

```text
How do AI agents differ from traditional automation systems?
```

### Test 3

```text
What are the core components of an Agentic Architecture?
```

### Test 4

```text
What role does memory play in Agentic AI workflows?
```

### Test 5

```text
Who won the 2022 FIFA World Cup?
```

The fifth question is intentionally outside the knowledge domain of the eBook.

The expected behavior is:

```text
I cannot answer based on the provided document.
```

---

## 19. Test Results

The RAG pipeline was tested through the FastAPI Swagger interface.

### Memory Question

Question:

```text
What role does memory play in Agentic AI workflows?
```

Result:

```text
PASS
```

The response explained long-term memory and short-term memory using retrieved eBook content.

### Agent vs Automation

Question:

```text
How do AI agents differ from traditional automation systems?
```

Result:

```text
PASS
```

The response described traditional automation as rule-based and repetitive and Agentic AI as goal-driven and autonomous.

### Agentic Architecture

Question:

```text
What are the core components of an Agentic Architecture?
```

Result:

```text
PASS
```

The response returned:

```text
Perception
Reasoning
Planning
Learning
Execution
```

### Out-of-Context Test

Question:

```text
Who won the 2022 FIFA World Cup?
```

Result:

```text
PASS
```

The chatbot responded:

```text
I cannot answer based on the provided document.
```

This demonstrates the intended document-grounding behavior.

### Note

The question:

```text
What is Agentic AI?
```

returned the refusal message even though relevant context was retrieved.

The retrieved context contained the relevant section, so this represents an area for future prompt/retrieval improvement rather than a retrieval failure.

---

## 20. API Testing with Swagger

Open:

```text
http://127.0.0.1:8000/docs
```

Then:

1. Find `POST /chat`
2. Click `Try it out`
3. Enter a question
4. Click `Execute`
5. Inspect the response

The response provides:

```text
Final Answer
Retrieved Context
Confidence Score
```

---

## 21. Error Handling

The API uses Pydantic request validation.

A valid request contains:

```json
{
  "query": "your question"
}
```

Invalid request data can return:

```text
422 Validation Error
```

---

## 22. Security

API keys are stored in `.env`.

The `.env` file is excluded from Git using:

```text
.env
```

Never place real API keys inside Python source files.

Never commit API keys to GitHub.

The repository contains `.env.example` with placeholder values.

---

## 23. Design Decisions

### Why Pinecone?

Pinecone provides vector storage and similarity search for the document embeddings.

### Why Sentence Transformers?

The assignment originally specifies OpenAI embeddings. Because OpenAI API credits were unavailable during development, a local Sentence Transformers model was used to generate embeddings without paid API calls.

### Why Groq?

Groq provides LLM inference through an API and can be integrated with LangChain.

### Why LangGraph?

LangGraph provides an explicit stateful workflow:

```text
START
 ↓
retrieve
 ↓
generate
 ↓
END
```

This keeps retrieval and generation as separate workflow nodes.

### Why FastAPI?

FastAPI provides a simple REST interface for sending user queries and receiving structured RAG responses.

---

## 24. Current Architecture

The final implementation uses:

```text
Document:
Agentic AI eBook

Embedding:
sentence-transformers/all-MiniLM-L6-v2

Embedding Dimension:
384

Vector Database:
Pinecone

Retrieval:
Top 3 chunks

Workflow:
LangGraph

LLM:
Groq openai/gpt-oss-20b

API:
FastAPI
```

---

## 25. Original Assignment vs Current Implementation

The original reference assignment specifies:

```text
OpenAI text-embedding-3-small
OpenAI gpt-4o-mini
```

The current implementation uses:

```text
sentence-transformers/all-MiniLM-L6-v2
Groq openai/gpt-oss-20b
```

The reason for this change is that OpenAI API credits were unavailable during development.

The following assignment components were retained:

- Python implementation
- PDF ingestion
- Document chunking
- Pinecone vector database
- LangGraph workflow
- Retrieval node
- Generation node
- Strict grounding
- FastAPI `/chat` endpoint
- Retrieved context output
- Confidence score output
- Benchmark testing
- Public GitHub repository

---

## 26. Future Improvements

Possible improvements include:

- Improve retrieval relevance scoring
- Use actual Pinecone similarity scores instead of a simple confidence heuristic
- Improve answer handling for short or ambiguous questions
- Add a Streamlit user interface
- Add automated tests
- Add conversation memory
- Add metadata filtering
- Add source/page references to retrieved chunks
- Improve prompt evaluation
- Add logging and monitoring

---

## 27. Running the Complete Project

### Step 1 — Activate virtual environment

```powershell
venv\Scripts\Activate.ps1
```

### Step 2 — Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 3 — Configure `.env`

Add:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-index
GROQ_API_KEY=your_groq_api_key
```

### Step 4 — Create Pinecone index

Use:

```text
Dimension: 384
Metric: cosine
```

### Step 5 — Run ingestion

```powershell
python -m src.ingestion
```

### Step 6 — Start API

```powershell
uvicorn app:app --reload
```

### Step 7 — Open Swagger

```text
http://127.0.0.1:8000/docs
```

### Step 8 — Test `/chat`

Example:

```json
{
  "query": "What role does memory play in Agentic AI workflows?"
}
```

---

## 28. Conclusion

This project demonstrates a complete Retrieval-Augmented Generation workflow using:

```text
PDF
 ↓
Chunking
 ↓
Local Embeddings
 ↓
Pinecone
 ↓
LangGraph Retrieval
 ↓
Groq LLM
 ↓
FastAPI
```

The chatbot is designed to remain grounded in the provided Agentic AI eBook and to refuse questions when the requested information is outside the retrieved document context.
