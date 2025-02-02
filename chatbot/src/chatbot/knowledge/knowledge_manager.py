import time
from typing import List

from chatbot.database.vector_store import VectorStore
from chatbot.knowledge.extractor import Extractor
from chatbot.knowledge.fetcher import Fetcher
from chatbot.knowledge.url_manager import UrlManager, URLStatus
from chatbot.models.document import Document


class KnowledgeManager:
    def __init__(self,
                 fetcher: Fetcher,
                 extractor: Extractor,
                 url_manager: UrlManager,
                 vector_store: VectorStore):
        self.fetcher = fetcher
        self.extractor = extractor
        self.url_manager = url_manager
        self.vector_store = vector_store

    def update_knowledge(self) -> bool:
        entry_url = "https://catalog.sonoma.edu/content.php?catoid=11&navoid=1431"
        self.url_manager.add_url(entry_url)
        while url := self.url_manager.get_next_url():
            self.url_manager.update_status(url, URLStatus.PROCESSING)
            document = self.fetcher.get_document(url)
            if document:
                self.vector_store.add_document(document)
                urls = self.extractor.get_urls(document)
                if urls:
                    self.url_manager.add_urls(urls)
                self.url_manager.update_status(url, URLStatus.CRAWLED)
            else:
                self.url_manager.update_status(url, URLStatus.FAILED)
            time.sleep(1)

        return False


    def retrieve_knowledge(self) -> List[Document]:
        pass
