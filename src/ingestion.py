from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from src.config import PINECONE_INDEX_NAME


def load_pdf(pdf_path: str):
    """Load the PDF and return its pages."""
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    return documents


def split_documents(documents):
    """Split the document pages into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def create_embeddings():
    """Create the OpenAI embedding model."""
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return embeddings


def create_vector_store(chunks, embeddings):
    """Store document chunks and embeddings in Pinecone."""
    vector_store = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME,
    )

    return vector_store


def run_ingestion(pdf_path: str):
    """Run the complete PDF ingestion pipeline."""
    documents = load_pdf(pdf_path)

    chunks = split_documents(documents)

    embeddings = create_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings,
    )

    return vector_store




if __name__ == "__main__":
    pdf_path = "data/Ebook-Agentic-AI.pdf"

    run_ingestion(pdf_path)

    print("Document ingestion completed successfully.")    