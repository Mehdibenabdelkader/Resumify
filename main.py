import typer
from rich import print
from rich.prompt import Prompt
import json
import weasyprint
import os

def storeDict(data_dict, filename):
    filename = os.path.basename(filename)
    if filename == '' or filename.startswith('.'):
        raise ValueError("Invalid filename")

    os.makedirs('data', exist_ok=True)

    with open(os.path.join('data', filename), 'w') as f:
        json.dump(data_dict, f)

def LoadDict(filename):
    with open(filename, 'r') as f:
        return json.load(f)

app = typer.Typer()

data = {
    "name": "mehdi",
    "role": "Software Engineer"
}



@app.command()
def main():
    startNew = typer.confirm("Start a new application?")
    data['name'] = (Prompt.ask("What's your name?")).capitalize()
    data['role'] = typer.prompt("What role are you applying for?")

    html = weasyprint.HTML('./resume2.html')
    html.write_pdf('./test.pdf')
    
    print("\n")
    print(f"[bold red]Hello[/bold red] {data['name']}")
    print(f"You are applying for the role of {data['role']}")

    storeDict(data, f"{data['name']}.json")

if __name__ == "__main__":
    app()