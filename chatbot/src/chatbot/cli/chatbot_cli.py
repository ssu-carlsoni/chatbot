import typer

from chatbot.database.vector_store import WeaviateVectorStore
from chatbot.knowledge.knowledge_manager import KnowledgeManager
from chatbot.knowledge.extractor import CatalogExtractor
from chatbot.knowledge.fetcher import Fetcher
from chatbot.knowledge.url_manager import UrlManager


app = typer.Typer()


@app.command()
def update_knowledge():
    fetcher = Fetcher()
    extractor = CatalogExtractor()
    url_manager = UrlManager()
    vector_store = WeaviateVectorStore(extractor)

    manager = KnowledgeManager(fetcher, extractor, url_manager, vector_store)
    if manager.update_knowledge():
        typer.echo("Knowledge Update Successful")
        raise typer.Exit(code=0)
    else:
        typer.echo("Knowledge Update Failed")
        raise typer.Exit(code=1)


@app.command()
def delete_knowledge():
    typer.echo("Not Implemented")
    raise typer.Exit(code=1)

if __name__ == "__main__":
    app()