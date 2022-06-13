from bs4 import BeautifulSoup as bs
from pathlib import Path
import re

dirpath = Path.gcw()

def scrape_html(html_name, html_page):
    newlines_re = re.compile('\\n( )?')
    id_regex = re.compile(' id=("\w*(-\w*)*?")')
    iframe_regex = re.compile('data-api-endpoint="\S*\s\S* ')
    src_regex = re.compile(f'(\.\/)\S*\D*\S*files\/')
    image_file_regex = re.compile('(\w{4})-\d-\d-\d-')
    syntax_re = re.compile('\\xa0')
    syntax_re = re.compile('\\u03c3')

    with open(f'{html_name}', 'rb') as f:
        soup = bs(f, 'html.parser')

        main_stuff = soup.find('div', {'class':'lds-content'})

        header = main_stuff.find_all('div')[1]
        header.find_all('span')[1].text

        intro = main_stuff.find_all('div')[5]

        intro_text = str(intro.get_text())
        intro_text = newlines_re.sub('', intro_text)
        intro_text = syntax_re.sub(' ', intro_text)
        intro_text = intro_text.replace('—', ' -- ')

        # Main content scrape
        main_body = main_stuff.find_all('div')[6]

        remove_these = main_body.find_all('iframe', {'allow':'autoplay *'})
        for iframe in remove_these:
            iframe.decompose()

        string = str(main_body)

        # Lots of text fixes
        body_text = newlines_re.sub(' ', string)
        body_text = id_regex.sub('', body_text)
        body_text = body_text.replace('<div>', '<div class="row">')
        body_text = iframe_regex.sub('', body_text)
        body_text = image_file_regex.sub('', body_text)
        body_text = src_regex.sub(f'{html_page}/', body_text)
        body_text = body_text.replace('<ul>', '<div><ul>')
        body_text = body_text.replace('</ul>', '</ul></div>')
        body_text = body_text.replace('<ol>', '<div><ol>')
        body_text = body_text.replace('</ol>', '</ol></div>')
        body_text = body_text.replace('<iframe', '<div><iframe')
        body_text = body_text.replace('</iframe>', '</iframe></div>')
        body_text = body_text.replace('<img', '<img class="fit center"')
        body_text = body_text.replace('—', ' -- ')
        body_text = body_text.replace('σ', '&sigma;')
        body_text = body_text.replace('∑', '&Sigma;')
        body_text = body_text.replace('−', '&minus;')

        body_text = syntax_re.sub(' ', body_text)

    return intro_text, body_text 

def this_is_a_generator():
    files = list(dirpath.glob('*.html'))
    files.append(None)
    for i in range(len(files)-1):
        intro_text, body_text = scrape_html(files[i].name, files[i].stem)
        try:
            pair = (files[i].stem, files[i+1].stem)
        except AttributeError:
            pair = (files[i].stem, None)
        yield files[i], pair[0], pair[1], intro_text, body_text

def create_html(file_path, current_file, next_file, header, body):
    with open(file_path, 'w') as out:
            out.write(f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Document</title>
            <link
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
                crossorigin="anonymous"
            />
            <style>
            * {{
                padding: 0;
                margin: 0;
            }}
            .fit {{ /* set relative picture size */
                max-width: 100%;
                max-height: 100%;
            }}
            .center {{
                display: block;
                margin: auto;
            }}
            a {{
                color: white;
            }}
            </style>
            </head>
            <body>
            <div class="container">
            <div class="row py-4">
            <div class="col">
            <h1>{current_file}</h1>
            </div>
            <div class="col">
            <button type="button" class="btn btn-primary align-baseline" href="{current_file}">Back</button>
            <button type="button" class="btn btn-primary align-baseline" href="{next_file}">Next</button>
            </div>
            </div>
            <div class="row">
            <p>{header}</p>
            </div>
            {body}
            </div>
            <div class="row py-4">
            <div class="col">
            <button type="button" class="btn btn-primary align-baseline" href="{current_file}">Back</button>
            <button type="button" class="btn btn-primary align-baseline" href="{next_file}">Next</button>
            </div>
            </div>
            </body>
            </html>
            ''')