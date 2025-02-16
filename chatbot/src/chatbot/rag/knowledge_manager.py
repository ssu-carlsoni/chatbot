import logging
from typing import List

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import TextSplitter


class KnowledgeManager:
    def __init__(
            self,
            logger: logging.Logger,
            document_loaders: List[BaseLoader],
            text_splitter: TextSplitter,
            vector_store: VectorStore,
    ):
        self.logger = logger
        self.document_loaders = document_loaders
        self.text_splitter = text_splitter
        self.vector_store = vector_store

    def rebuild(self) -> bool:
        self.vector_store.delete()
        self.logger.info("Knowledge deleted")
        self.logger.info("Starting to load knowledge")
        for loader in self.document_loaders:
            self.logger.info(f"Loading documents from {loader.__class__.__name__}")
            documents = loader.load()
            self.logger.info(f"Loaded {len(documents)} documents")
            splits = self.text_splitter.split_documents(documents)
            self.logger.info(f"Documents split into {len(splits)} parts")
            self.logger.info('Adding splits documents to vector store',
                             extra={'loader': loader.__class__.__name__})
            self.vector_store.add_documents(documents=splits)
            self.logger.info('Split documents added to vector store',
                             extra={'loader': self.__class__.__name__})
        return True

    def retrieve(self, search: str) -> List[Document]:
        retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 6,
                "score_threshold": 0.5,
            })
        return retriever.invoke(search)
