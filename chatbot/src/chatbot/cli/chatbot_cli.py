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


@app.command()
def chat():
    typer.echo("To be implemented")
    pass


if __name__ == "__main__":
    app()
