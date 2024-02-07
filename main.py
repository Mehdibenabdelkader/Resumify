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

    data = {
    "FullName": "mehdi",
    "Role": "Software Engineer"
    }
    
    startNew = typer.confirm("Start a new application?")
    data['FullName'] = (Prompt.ask("What's your name?")).capitalize()
    data['Role'] = typer.prompt("What role are you applying for?")

    print("\n")
    print(f"[bold red]Hello[/bold red] {data['FullName']}")
    print(f"You are applying for the role of {data['Role']}")

    storeDict(data, f"{data['FullName']}.json")

    # Read the JSON file
    with open(f"./data/{data['FullName']}.json") as json_file:
        data = json.load(json_file)

    # Read the HTML template
    with open('./Template.html') as template_file:
        template_content = template_file.read()

    # Replace placeholder values in the template
    for key, value in data.items():
        placeholder = '{{' + key + '}}'
        template_content = template_content.replace(placeholder, str(value))

    # Write the updated HTML content to a new file
    with open('output.html', 'w') as output_file:
        output_file.write(template_content)

    # Convert HTML to PDF
    weasyprint.HTML('output.html').write_pdf('output.pdf')
    os.remove('output.html')

if __name__ == "__main__":
    app()