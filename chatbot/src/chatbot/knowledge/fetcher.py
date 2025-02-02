from typing import Optional

import httpx

from chatbot.models.document import Document


class Fetcher:
    @staticmethod
    def get_document(url: str) -> Optional[Document]:
        response = httpx.get(url)
        if response.status_code != 200:
            return None
        return Document(url=url, raw_content=response.content.decode('utf-8'))
