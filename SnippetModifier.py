from bs4 import BeautifulSoup

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
