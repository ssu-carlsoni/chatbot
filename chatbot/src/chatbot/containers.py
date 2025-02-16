import logging
import sys

from dependency_injector import containers, providers
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import weaviate

from chatbot.rag.document_loaders.courses_csv_loader import CoursesCSVLoader
from chatbot.rag.knowledge_manager import KnowledgeManager
from chatbot.storage.weaviate_vector_store import WeaviateVectorStore


def init_weaviate_client(
    http_host: str,
    http_port: int,
    http_secure: bool,
    grpc_host: str,
    grpc_port: int,
    grpc_secure: bool,
):
    client = weaviate.connect_to_custom(
        http_host=http_host,
        http_port=http_port,
        http_secure=http_secure,
        grpc_host=grpc_host,
        grpc_port=grpc_port,
        grpc_secure=grpc_secure,
    )
    yield client
    client.close()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    config.from_yaml(filepath="./config.example.yml", required=True)
    config.from_yaml(filepath="./config.yml", required=True)

    logging_config = providers.Resource(
        logging.basicConfig,
        level=logging.INFO,
        stream=sys.stdout,
    )

    # Document Loaders
    course_csv_loader = providers.Factory(
        CoursesCSVLoader,
        file_path=config.data_sources.course_csv_file(),
    )
    # List of document loaders for KnowledgeManager
    document_loaders = providers.List(
        course_csv_loader,
    )

    # Text Splitter for Document Embedding
    text_splitter = providers.Factory(
        RecursiveCharacterTextSplitter,
        chunk_size=config.text_splitter.chunk_size(),
        chunk_overlap=config.text_splitter.chunk_overlap(),
        add_start_index=config.text_splitter.add_start_index(),
    )

    # Embeddings for Document Vectorization
    embedding = providers.Factory(
        HuggingFaceEmbeddings,
        model_name=config.huggingface.embedding_model_name(),
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False},
    )

    # Weaviate Client for Vector Store
    weaviate_client = providers.Resource(
        init_weaviate_client,
        http_host=config.weaviate.http_host(),
        http_port=config.weaviate.http_port(),
        http_secure=config.weaviate.http_secure(),
        grpc_host=config.weaviate.grpc_host(),
        grpc_port=config.weaviate.grpc_port(),
        grpc_secure=config.weaviate.grpc_secure(),
    )

    # Vector Store for KnowledgeManager
    vector_store = providers.Factory(
        WeaviateVectorStore,
        client=weaviate_client,
        embedding=embedding,
        index_name="ssu_chatbot",
        text_key="text",
    )

    # Knowledge Manager for RAG
    knowledge_manager = providers.Factory(
        KnowledgeManager,
        logger=providers.Factory(
            logging.getLogger,
            "rag.KnowledgeManager"
        ),
        document_loaders=document_loaders,
        text_splitter=text_splitter,
        vector_store=vector_store,
    )
