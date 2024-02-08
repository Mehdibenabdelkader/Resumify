import typer
from rich import print
from rich.prompt import Prompt
import json
import weasyprint
import os
from bs4 import BeautifulSoup


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
    

def addSnippet(template, Section, Counter):
    # Read the HTML file
    with open(template, 'r') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a new HTML snippet
    snippet = '''
    <h4>{{Degree'''+ Counter + '''}}</h4>
        <p>
            {{School'''+ Counter + '''}}<br />
            {{Year'''+ Counter + '''}}
        </p>
    '''

    # Find the specific place where you want to insert the new element
    target_element = soup.find(id=Section)  # Assuming you have an element with id 'target'

    # Insert the new snippet after the target element
    target_element.insert_after(BeautifulSoup(snippet, 'html.parser'))
    target_element.insert_after('\n')
    # Insert the new element before the target element

    # Write the modified HTML content back to the file
    with open(template, 'w') as file:
        file.write(str(soup))

app = typer.Typer()


@app.command()
def main():

    degreeCounter = 1

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

        print("\n")
        print("This section is about your education")

        data[f'Degree{degreeCounter}'] = typer.prompt("What's your degree?")
        data[f'School{degreeCounter}'] = typer.prompt("What's the name of your school?")
        data[f'Year{degreeCounter}'] = typer.prompt("What year did you graduate?")
        
        newDegree = typer.confirm("Do you have another degree?")
        while newDegree:
            degreeCounter += 1
            addSnippet('Template.html', 'Education', str(degreeCounter))
            data[f'Degree{degreeCounter}'] = typer.prompt("What's your degree?")
            data[f'School{degreeCounter}'] = typer.prompt("What's the name of your school?")
            data[f'Year{degreeCounter}'] = typer.prompt("What year did you graduate?")
            newDegree = typer.confirm("Do you have another degree?")

        



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