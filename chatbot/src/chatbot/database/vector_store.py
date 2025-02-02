import os
import urllib
from abc import ABC, abstractmethod
from typing import List

import weaviate
import weaviate.classes.config as wc
from weaviate.exceptions import WeaviateBaseError

from chatbot.knowledge.extractor import Extractor
from chatbot.models.document import Document
from chatbot.models.query import Query


# VectorStore Interface
class VectorStore(ABC):

    @abstractmethod
    def create_collection(self) -> bool:
        pass

    @abstractmethod
    def delete_collection(self) -> bool:
        pass

    @abstractmethod
    def add_document(self, document: Document) -> bool:
        pass

    @abstractmethod
    def retrieve(self, query: Query) -> List[Document]:
        pass


class WeaviateVectorStore(VectorStore):
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
        self.client = None


    def get_client(self) -> weaviate.client:
        if self.client is None:
            self.client = weaviate.connect_to_custom(
                http_host="weaviate",
                http_port=8080,
                http_secure=False,
                grpc_host="weaviate",
                grpc_port=50051,
                grpc_secure=False,
            )
        return self.client


    def close_client(self):
        if self.client is not None:
            self.client.close()
            self.client = None


    def create_collection(self) -> bool:
        try:
            self.get_client().collections.create(
                name="Knowledge",
                properties=[
                    wc.Property(name="node_id", data_type=wc.DataType.INT),
                    wc.Property(name="title", data_type=wc.DataType.TEXT),
                    wc.Property(name="url", data_type=wc.DataType.TEXT),
                    wc.Property(name="content", data_type=wc.DataType.TEXT),
                ],
                # Define the vectorizer module (none, using our own vectors)
                vectorizer_config=wc.Configure.Vectorizer.none(),
                # Define the generative module
                # generative_config=wc.Configure.Generative.none()
            )
            self.close_client()
            return True
        except WeaviateBaseError:
            return False


    def delete_collection(self) -> bool:
        try:
            self.get_client().collections.delete("Knowledge")
            self.close_client()
            return True
        except WeaviateBaseError:
            return False


    def add_document(self, document: Document) -> bool:
        vector_content = self.extractor.get_search_content(document)

        filename = self.sanitize_filename(document.url)
        directory = "data"
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)

        # Write the text to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(vector_content)

        print(f"Text from {document.url} has been written to {filepath}")
        return True


    def retrieve(self, query: Query) -> List[Document]:
        pass


    @staticmethod
    def sanitize_filename(url: str) -> str:
        # Parse the URL and query string
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path.replace('/', '_')  # Replace / with _
        query = urllib.parse.quote(parsed_url.query,
                                   safe='_')  # Safely encode query string

        # Combine path and query for filename
        filename = f"{parsed_url.netloc}{path}"
        if query:
            filename += f"_{query}"

        # Truncate the filename if it's too long and add .txt extension
        return filename[
               :255] + ".txt"  # Max filename length for most filesystems

# VectorStore Factory
def create() -> VectorStore:
    return WeaviateVectorStore()