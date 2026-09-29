from typing import List, TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from src.config import PINECONE_INDEX_NAME


class AgentState(TypedDict):
    question: str
    context: List[str]
    answer: str
    score: float


def build_rag_graph():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
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
You are a strict RAG assistant.

Answer the user's question using ONLY the information
contained in the provided context.

If the context does not contain enough information to
answer the question, say:

"I cannot answer based on the provided document."

Do not use outside knowledge.
Do not make up facts.

Context:
{context}

Question:
{state["question"]}
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