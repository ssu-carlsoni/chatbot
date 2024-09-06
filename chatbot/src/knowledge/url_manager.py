from typing import Dict, List, Optional
from enum import Enum


class URLStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    CRAWLED = "crawled"
    FAILED = "failed"


class UrlManager:
    def __init__(self):
        self._urls: Dict[str, URLStatus] = {}

    def add_url(self, url: str) -> None:
        if url not in self._urls:
            self._urls[url] = URLStatus.PENDING

    def add_urls(self, urls: List[str]) -> None:
        for url in urls:
            if url not in self._urls:
                self._urls[url] = URLStatus.PENDING

    def update_status(self, url: str, status: URLStatus) -> None:
        if url in self._urls:
            self._urls[url] = status

    def get_status(self, url: str) -> Optional[URLStatus]:
        return self._urls.get(url)

    def get_next_url(self) -> Optional[str]:
        for url, status in self._urls.items():
            if status == URLStatus.PENDING:
                return url
        return None

    def count(self) -> int:
        return len(self._urls)
