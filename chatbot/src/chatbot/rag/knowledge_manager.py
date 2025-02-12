import logging
from typing import List

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore


class KnowledgeManager:
    def __init__(
            self,
            logger: logging.Logger,
            vector_store: VectorStore,
    ):
        self.logger = logger
        self.vector_store = vector_store

    def reload_knowledge(self, loaders: List[BaseLoader]) -> bool:
        self.vector_store.delete()
        self.logger.info("Knowledge deleted")
        self.logger.info("Loading knowledge")
        for loader in loaders:
            self.vector_store.add_documents(documents=loader.load())
            self.logger.info('knowledge loaded',
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
