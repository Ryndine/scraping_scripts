from pydoc import replace
from packaging.version import parse as parseVersion
from fs.osfs import OSFS # operating system filesystem
from fs.walk import Step
from bs4 import BeautifulSoup as bs


_dir = '' # Starting directory

# Arguments for walk
exclude_dir = ['.git'] 
exclude_file = ['*.py', '.gitignore', '*.md', '*.zip', '*.ipynb']
depth = 2

def scrapeContent(path):
    with open(path, 'rb') as file:
        soup = bs(file, 'html.parser')

        #Module id
        content = soup.find('div', {'id':'wiki_page_show'})
        # Challenge id
        if content is None:
            content = soup.find('div', {'id':'bootcamp'})

        stylesheets = soup.find_all('link', {'rel':'stylesheet'})
        # Doesn't always work, too lazy to fix atm
        # css_formatted = '{0[0]}\n{0[1]}\n{0[2]}\n{0[3]}\n{0[4]}\n{0[5]}'.format(stylesheets)

    return content, stylesheets

def replaceCollapse(path):
    with open(path, 'r', encoding="utf-8") as file:
        readFile = file.read()

    replaceCollapse = readFile.replace(' collapse', '')

    with open(path, 'w', encoding="utf-8") as file:
        file.write(replaceCollapse)

def createHTML(path, prevFile, currFile, nextFile, style, content):
    with open(path, 'w', encoding="utf-8") as w:
        w.write(f'''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{currFile}</title>
        <style>
            #updated_buttons {{
                height: 200px;
                display: flex;
                align-items: start;
                justify-content: space-evenly;
                }}
            a.buttons {{
                text-decoration: none;
                border-radius: 10%;
                color: rgb(255, 255, 255);
                background-color: rgb(50, 111, 168);
                display: inline-block;
                padding: 8px 16px;
                }}

            a.buttons:hover {{
                background-color: #ddd;
                color: black;
                border-radius: 10%;
                }}
        </style>
        {style}
    </head>
    <body>
        {content.prettify()}
        <div id="updated_buttons">
            <a class="buttons" href="{prevFile}">Back</a>
            <a class="buttons" href="{nextFile}">Next</a>
        </div>
    </body>
</html>
''')

with OSFS(_dir) as pfs: # create osfs. the path you pass to the constructor is the root of this filesystem
    w: Step # Step is each level of the walk
    for w in pfs.walk.walk('/', exclude_dirs=exclude_dir ,exclude=exclude_file, max_depth=depth): # walk recursively. definitely look at all of the available keyword arguments
        cur_path = w.path # the relative path of the current directory in the walk process
        # print(cur_path)
        dir_files: list = w.files # a list of the files at this path
        # print(dir_files)
        # dir_files.sort(key=natural_keys) # list sort is in place, don't reassign
        dir_files.sort(key=lambda x: parseVersion(x.name)) # list sort is in place, don't reassign
        nfiles = len(dir_files)
        # print(cur_path)

        # Loop to be used in the HTML creation
        for i in range(nfiles):
            # Previous for back button
            prev_file = dir_files[i-1] if i > 0 else None
            if prev_file != None:
                previous_button = prev_file.name
            else:
                previous_button = None

            # Current file
            this_file = dir_files[i]

            # Next for next button
            next_file = dir_files[i+1] if i < nfiles-1 else None
            if next_file != None:
                next_button = next_file.name
            else:
                next_button = None

            # Find paths
            relative_path = this_file.make_path(cur_path)
            os_path = pfs.getsyspath(relative_path)

            # print("\t", previous_button, this_file.name, next_button)
            print(this_file)

            content, stylesheets = scrapeContent(os_path)    

            createHTML(os_path, previous_button, this_file, next_button, stylesheets, content)

            replaceCollapse(os_path)