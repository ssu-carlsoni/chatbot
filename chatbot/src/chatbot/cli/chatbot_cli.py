import typer
from async_typer import AsyncTyper

from chatbot.containers import Container


app = AsyncTyper()
container = Container()


@app.async_command()
async def rebuild_knowledge():
    return_code = 0
    await container.init_resources()
    manager = await container.knowledge_manager()
    if manager.rebuild():
        print("Knowledge Rebuilt Successfully")
    else:
        print("Knowledge Rebuild Failed")
        return_code = 1
    await container.shutdown_resources()
    raise typer.Exit(code=return_code)


@app.async_command()
async def retrieve_knowledge(question: str):
    return_code = 0
    await container.init_resources()
    manager = await container.knowledge_manager()
    documents = manager.retrieve(question)
    for doc in documents:
        print(doc)
        print("\n\n----\n\n")
    await container.shutdown_resources()
    raise typer.Exit(code=return_code)


if __name__ == "__main__":
    app()
