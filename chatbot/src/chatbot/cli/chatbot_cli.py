import typer

from chatbot.containers import Container


app = typer.Typer()
container = Container()


@app.command()
def update_knowledge():
    manager = container.knowledge_manager()
    if manager.update_knowledge():
        typer.echo("Knowledge Update Successful")
        raise typer.Exit(code=0)
    else:
        typer.echo("Knowledge Update Failed")
        raise typer.Exit(code=1)


@app.command()
def rebuild_knowledge():
    typer.echo("Not Implemented")
    raise typer.Exit(code=1)

if __name__ == "__main__":
    app()