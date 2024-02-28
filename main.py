import typer
from rich import print
from rich.prompt import Prompt
import json
import weasyprint
import os
from DataLoading import *
import shutil
from jinja2 import Environment, FileSystemLoader

app = typer.Typer()

def render_template(template_path, data):
    """Render Jinja2 template with the provided data."""
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    rendered_template = template.render(data)
    return rendered_template

@app.command()
def main():
    startNew = typer.confirm("Start a new application?")
    
    if startNew:
        degreeCounter = 1
        skillCounter = 1
        languageCounter = 1

        data = {
        "FullName": "mehdi",
        "Role": "Software Engineer"
        }

        data['FullName'] = (Prompt.ask("What's your name?")).capitalize()
        data['Role'] = typer.prompt("What role are you applying for?")
        data['Email'] = typer.prompt("What's your email?")
        data['Adress'] = typer.prompt("Where do you live? (City, Country)")
        data['Number'] = typer.prompt("What's your phone number?")

    
        print("\n")
        print("This section is about your education")

        newDegree = typer.confirm("Do you want to add a degree?")
        degrees = []
        while newDegree:
            degree = {}
            degree[f'Degree'] = typer.prompt("What's your degree?")
            degree[f'School'] = typer.prompt("What's the name of your school?")
            degree[f'Year'] = typer.prompt("What year did you graduate?")
            degrees.append(degree)
            newDegree = typer.confirm("Do you have another degree?")

        data["Degrees"] = degrees

        print("\n")
        print("This section is about your skills and tools")

        newSkill = typer.confirm("Do you want to add a skill?")
        skills = []
        while newSkill:
            skill = {}
            skill[f'Skill'] = typer.prompt("What's your skill?")
            skill[f'Tools'] = typer.prompt("What tools do you master?")
            skills.append(skill)
            newSkill = typer.confirm("Do you want to add a skill?")

        data["Skills"] = skills

        print("\n")
        print("This section is about your languages")

        
        newLanguage = typer.confirm("Do you want to add a language?")
        Languages = []
        while newLanguage:
            Language = {}
            Language[f'Language'] = typer.prompt("What language do you speak?")
            Language[f'Level'] = typer.prompt("What's your level?")
            Languages.append(Language)
            newLanguage = typer.confirm("Do you want to add a language?")

        data["Languages"] = Languages


        print("\n")
        print("This section is about your proffessional experiences")

        newExperience = typer.confirm("Do you want to add an experience?")
        Experiences = []
        while newExperience:
            Experience = {}
            Experience[f'Position'] = typer.prompt("What position were you in?")
            Experience[f'Year'] = typer.prompt("What year did you start?")
            Experience[f'Company'] = typer.prompt("In what Company?")
            Experience[f'Description'] = typer.prompt("Enter a short description of your work")
            Experiences.append(Experience)
            newExperience = typer.confirm("Do you want to add a language?")

        data["Experiences"] = Experiences


        print("\n")
        print("This section is about your certifications")

        newCertification = typer.confirm("Do you want to add a certification?")
        Certifications = []
        while newCertification:
            Certification = {}
            Certification[f'Name'] = typer.prompt("What's the name of the certification?")
            Certification[f'Platform'] = typer.prompt("What's the plateform?")
            Certifications.append(Certification)
            newCertification = typer.confirm("Do you want to add a certification?")

        data["Certifications"] = Certifications
            
        print("\n")
        print("This section is about your projects")

        newProject = typer.confirm("Do you want to add a project?")
        Projects = []
        while newProject:
            Project = {}
            Project[f'Name'] = typer.prompt("What's your project name?")
            Project[f'Description'] = typer.prompt("Describe your project")
            Projects.append(Project)
            newProject = typer.confirm("Do you want to add a project?")

        data["Projects"] = Projects

        print("\n")
        print(f"[bold red]Hello[/bold red] {data['FullName']}")
        print(f"You are applying for the role of {data['Role']}")

        storeDict(data, f"{data['FullName']}.json")
        FileName = data['FullName']
    
    else:
        Files = os.listdir("./data")
        print("\n")
        print(f"[bold green]Files in repository :[/bold green]")
        for file in Files:
            print(file)

        print("\n")
        FileName = (Prompt.ask("Pick a file")).capitalize()
        
        # Check if the JSON file exists
        json_file_path = f"./data/{FileName}.json"
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"JSON file '{json_file_path}' does not exist.")

    # Read the JSON file
    with open(f"./data/{FileName}.json") as json_file:
        data = json.load(json_file)

    # Render the template - make this dynamic
    template_path = './Template.html'  # Path to your Jinja2 template file
    rendered_template = render_template(template_path, data)

    # Output or save the rendered template as needed
    output_file = 'output.html'  # Path to the output HTML file
    with open(output_file, 'w') as f:
        f.write(rendered_template)

    # Convert HTML to PDF and remove the temporary files
    weasyprint.HTML('output.html').write_pdf('output.pdf')
    os.remove('output.html')

if __name__ == "__main__":
    app()