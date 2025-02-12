import typer

from chatbot.containers import Container

app = typer.Typer()
container = Container()


@app.command()
def update_knowledge():
    return_code = 0
    loaders = [container.course_csv_loader()]
    manager = container.knowledge_manager()
    if manager.reload_knowledge(loaders=loaders):
        typer.echo("Knowledge Update Successful")
    else:
        typer.echo("Knowledge Update Failed")
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
