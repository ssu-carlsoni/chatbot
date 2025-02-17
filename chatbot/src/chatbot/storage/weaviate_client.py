from typing import AsyncGenerator

from langchain.vectorstores import weaviate
import weaviate
from weaviate import WeaviateClient


async def init_weaviate_client(
    http_host: str,
    http_port: int,
    http_secure: bool,
    grpc_host: str,
    grpc_port: int,
    grpc_secure: bool,
) -> AsyncGenerator[WeaviateClient, None]:
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