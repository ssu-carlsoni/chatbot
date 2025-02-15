import typer

from chatbot.containers import Container

app = typer.Typer()
container = Container()


@app.command()
def knowledge_rebuild():
    return_code = 0
    manager = container.knowledge_manager()
    if manager.rebuild():
        typer.echo("Knowledge Rebuilt Successful")
    else:
        typer.echo("Knowledge Rebuild Failed")
        return_code = 1
    container.shutdown_resources()
    raise typer.Exit(code=return_code)


@app.command()
def test_question():
    manager = container.knowledge_manager()
    question = "What are the math course are offered?"
    documents = manager.retrieve(question)
    for doc in documents:
        typer.echo(doc.metadata)
    container.shutdown_resources()
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
