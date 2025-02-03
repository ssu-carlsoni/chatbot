import logging
import sys

from dependency_injector import containers, providers

from chatbot.database.vector_store import WeaviateVectorStore
from chatbot.knowledge.extractor import CatalogExtractor
from chatbot.knowledge.fetcher import Fetcher
from chatbot.knowledge.knowledge_manager import KnowledgeManager
from chatbot.knowledge.url_manager import UrlManager


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["../../config.example.yml",
                                                 "../../config.local.yml"])

    logging = providers.Resource(
        logging.basicConfig,
        level=logging.INFO,
        stream=sys.stdout,
    )

    fetcher = providers.Factory(Fetcher)
    extractor = providers.Factory(CatalogExtractor)
    url_manager = providers.Factory(UrlManager)

    vector_store = providers.Factory(WeaviateVectorStore, extractor=extractor)

    knowledge_manager = providers.Factory(
        KnowledgeManager,
        fetcher=fetcher,
        extractor=extractor,
        url_manager=url_manager,
        vector_store=vector_store,
    )
