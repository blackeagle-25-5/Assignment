from typing import List, TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore

from src.config import PINECONE_INDEX_NAME, GROQ_API_KEY


class AgentState(TypedDict):
    question: str
    context: List[str]
    answer: str
    score: float


def build_rag_graph():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-20b",
        temperature=0,
    )

    def retrieve_node(state: AgentState):
        docs = retriever.invoke(state["question"])

        context_texts = [
            document.page_content
            for document in docs
        ]

        return {
            "context": context_texts
        }

    def generate_node(state: AgentState):
        context = "\n\n".join(state["context"])

        prompt = f"""
You are a document-grounded RAG assistant.

Your job is to answer the user's question using ONLY
the retrieved context from the Agentic AI eBook.

IMPORTANT RULES:
1. Use the retrieved context as the source of truth.
2. If the context contains information that answers the
   question, provide a clear and concise answer.
3. You may combine information from multiple retrieved
   chunks when necessary.
4. Do not use outside knowledge.
5. Do not invent or assume facts.
6. If the retrieved context genuinely does not contain
   enough information to answer the question, respond:

"I cannot answer based on the provided document."

Retrieved context:
------------------
{context}
------------------

User question:
{state["question"]}

Answer:
"""

        response = llm.invoke(prompt)

        if state["context"]:
            score = 0.95
        else:
            score = 0.0

        return {
            "answer": response.content,
            "score": score,
        }

    workflow = StateGraph(AgentState)

    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()