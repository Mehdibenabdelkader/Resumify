import typer
from rich import print
from rich.prompt import Prompt
import json
import weasyprint
import os
from DataLoading import *
from SnippetModifier import *
import shutil

app = typer.Typer()


@app.command()
def main():

    degreeCounter = 1
    skillCounter = 1
    languageCounter = 1

    data = {
    "FullName": "mehdi",
    "Role": "Software Engineer"
    }
    
    startNew = typer.confirm("Start a new application?")
    if startNew:
        data['FullName'] = (Prompt.ask("What's your name?")).capitalize()
        data['Role'] = typer.prompt("What role are you applying for?")
        data['Email'] = typer.prompt("What's your email?")
        data['Adress'] = typer.prompt("Where do you live? (City, Country)")
        data['Number'] = typer.prompt("What's your phone number?")

        
        
            

        


        shutil.copy('Template.html', 'temp.html')
        print("\n")
        print(f"[bold red]Hello[/bold red] {data['FullName']}")
        print(f"You are applying for the role of {data['Role']}")

        storeDict(data, f"{data['FullName']}.json")

        # Read the JSON file
        with open(f"./data/{data['FullName']}.json") as json_file:
            data = json.load(json_file)

        # Read the HTML template
        with open('./temp.html') as template_file:
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