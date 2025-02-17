from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from langchain.chains import ConversationalRetrievalChain

from chatbot.containers import Container
from chatbot.web.endpoints import router


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(fastapi: FastAPI) -> AsyncGenerator[None, None]:
        container = Container()
        try:
            await container.init_resources()
            fastapi.container = container
            yield
        finally:
            await container.shutdown_resources()

    application = FastAPI(lifespan=lifespan)
    application.mount(
        "/static",
        StaticFiles(directory="src/chatbot/web"),
        name="static",
    )
    application.include_router(router)
    return application


# Create the FastAPI application
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)