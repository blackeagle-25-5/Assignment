
# Agentic AI RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with Python, LangChain, LangGraph, OpenAI, Pinecone, and FastAPI.

The chatbot uses the provided **Agentic AI eBook** as its knowledge source and is designed to answer questions using only information retrieved from that document.

---

## 1. Project Objective

The goal of this project is to build a RAG-based AI chatbot that:

- Loads the Agentic AI eBook.
- Splits the document into smaller text chunks.
- Converts the chunks into embedding vectors.
- Stores the vectors in Pinecone.
- Retrieves relevant chunks for a user question.
- Uses LangGraph to orchestrate the RAG workflow.
- Generates an answer based only on the retrieved context.
- Returns the answer, retrieved context, and confidence score through a FastAPI endpoint.

---

## 2. Technology Stack

- Python 3.10+
- LangChain
- LangGraph
- OpenAI
- Pinecone
- PyPDF
- FastAPI
- Uvicorn
- python-dotenv

---

## 3. Project Structure

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
├── .env
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
├── tests_sample_queries.py
└── README.md
````

---

## 4. Setup

### Step 1: Clone the repository

```bash
git clone <your-github-repository-url>
cd Assignment
```

### Step 2: Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### Step 3: Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 5. Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-index
```

The `.env` file contains secret API credentials and must not be committed to GitHub.

A `.env.example` file is included as a template.

---

## 6. Knowledge Source

The chatbot uses the provided Agentic AI eBook:

```text
data/Ebook-Agentic-AI.pdf
```

The PDF is loaded using `PyPDFLoader`.

The document is then split into chunks using:

```text
chunk_size = 1000
chunk_overlap = 200
```

---

## 7. Document Ingestion Pipeline

The ingestion pipeline is implemented in:

```text
src/ingestion.py
```

The pipeline follows these steps:

```text
Agentic AI PDF
      ↓
PDF Loading
      ↓
Document Pages
      ↓
Text Chunking
      ↓
OpenAI Embeddings
      ↓
Pinecone Vector Store
```

The embedding model used is:

```text
text-embedding-3-small
```

---

## 8. RAG Workflow

The RAG workflow is implemented using LangGraph in:

```text
src/graph.py
```

The workflow is:

```text
START
  ↓
Retrieve
  ↓
Generate
  ↓
END
```

### Retrieve

The user's question is used to search Pinecone for the most relevant document chunks.

The current retriever uses:

```text
k = 3
```

meaning that the top three relevant chunks are retrieved.

### Generate

The retrieved chunks are provided to the language model.

The model is instructed to:

* Use only the retrieved context.
* Avoid outside knowledge.
* Avoid inventing information.
* State that the document does not contain enough information when appropriate.

---

## 9. State Management

The LangGraph state contains:

```python
class AgentState(TypedDict):
    question: str
    context: List[str]
    answer: str
    score: float
```

The state stores:

* User question
* Retrieved context
* Generated answer
* Confidence score

---

## 10. FastAPI

The API is implemented in:

```text
app.py
```

Start the API using:

```powershell
uvicorn app:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 11. Chat Endpoint

The main endpoint is:

```text
POST /chat
```

### Request

```json
{
  "query": "What is Agentic AI according to the eBook?"
}
```

### Response

```json
{
  "final_answer": "Generated answer based on retrieved context.",
  "retrieved_context": [
    "Retrieved document chunk 1",
    "Retrieved document chunk 2",
    "Retrieved document chunk 3"
  ],
  "confidence_score": 0.95
}
```

The response contains:

1. Final generated answer
2. Retrieved context chunks
3. Confidence score

---

## 12. Grounding Behaviour

The chatbot is designed to answer questions only from the provided document.

If the retrieved context does not contain enough information, the chatbot should respond:

```text
I cannot answer based on the provided document.
```

This prevents the chatbot from intentionally using outside knowledge to answer unsupported questions.

---

## 13. Test Queries

The benchmark queries are stored in:

```text
tests_sample_queries.py
```

The test questions include:

```text
1. What is Agentic AI according to the eBook?

2. How do AI agents differ from traditional automation systems?

3. What are the core components of an Agentic Architecture?

4. What role does memory play in Agentic AI workflows?

5. Who won the 2022 FIFA World Cup?
```

The final question is an out-of-context validation test. The expected behaviour is that the system should not answer it using external knowledge.

---

## 14. Running the Project

### Ingest the document

The ingestion pipeline should be executed after the Pinecone index and API credentials have been configured.

```powershell
python -m src.ingestion
```

### Start the API

```powershell
uvicorn app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Use the `/chat` endpoint to test the chatbot.

---

## 15. Example Questions

Example request:

```json
{
  "query": "What is Agentic AI according to the eBook?"
}
```

Another example:

```json
{
  "query": "What role does memory play in Agentic AI workflows?"
}
```

Out-of-context example:

```json
{
  "query": "Who won the 2022 FIFA World Cup?"
}
```

The system should avoid answering questions that cannot be supported by the retrieved document context.

---

## 16. Security

API keys are stored in:

```text
.env
```

The `.env` file is excluded from Git using `.gitignore`.

Never commit real API keys to the GitHub repository.

The `.env.example` file contains only placeholder values.

---

## 17. Architecture Overview

```text
                    ┌─────────────────────┐
                    │   Agentic AI PDF    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PDF Loader       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Chunking     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ OpenAI Embeddings   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Pinecone       │
                    │   Vector Database    │
                    └──────────┬──────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │ LangGraph Retrieve  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ LangGraph Generate  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI         │
                    │ Answer + Context    │
                    │ + Confidence Score  │
                    └─────────────────────┘
```

---

## 18. Current Implementation

The project currently contains:

* PDF loading
* Document chunking
* OpenAI embedding configuration
* Pinecone vector-store configuration
* LangGraph retrieval and generation workflow
* FastAPI `/chat` endpoint
* Benchmark queries
* Environment configuration
* Project documentation

---

## 19. Future Improvements

Possible improvements include:

* Better confidence scoring based on retrieval similarity.
* Improved prompt engineering.
* Metadata filtering.
* More advanced retrieval strategies.
* Conversation history.
* Streaming responses.
* Streamlit chat interface.
* Automated evaluation of benchmark queries.

---



