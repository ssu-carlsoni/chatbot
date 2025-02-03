from typing import Optional

import httpx

from chatbot.models.web import WebDocument


class Fetcher:
    @staticmethod
    def get_document(url: str) -> Optional[WebDocument]:
        response = httpx.get(url)
        if response.status_code != 200:
            return None
        return WebDocument(url=url, raw_content=response.content.decode('utf-8'))
