import typer


app = typer.Typer()

@app.command()
def main():
    typer.echo("Welcome to the chatbot CLI")
