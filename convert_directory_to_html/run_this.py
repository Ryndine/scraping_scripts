from scraping_functions import this_is_a_generator, create_html
from clean_up import clean_directory

if __name__ == '__main__':
    clean_directory()
    # yield files[i], pair[0], pair[1], intro_text, body_text
    for a, b, c, d, e in this_is_a_generator():
        # create_html(module_file, current_module, next_module, header, body)
        create_html(a, b, c, d, e)