#!python3

import json
import math

COLCOUNT = 4


def main():
    data = read_content()
    toc_section = create_toc_code(data)
    links_section = create_links_code(data)
    process_template(toc_section, links_section)


def read_content():
    '''
    Read the content from the json file and return it as a list of
    link categories, each with a list of individual links
    '''
    with open('content.json', 'r') as infile:
        return json.load(infile)


def create_toc_code(data):
    '''
    Create the html code for the table of contents
    (the panel on the left side)
    '''
    toc_section = ''
    for category in data:
        name, bookmark = extract_from_dict(category, 'name', 'bookmark')
        print(f'----\n  Name    : {name}\n  Bookmark: {bookmark}')
        toc_section += f'            <li><a href="#{bookmark}">{name}</a></li>\n'
    return toc_section


def create_links_code(data):
    '''
    Create the html code for the actual links on the start page
    Grouped per category, in an N-column table; N is determined
    by the constant COLCOUNT
    '''
    result = []
    for category in data:
        name, bookmark = extract_from_dict(category, 'name', 'bookmark')
        result.append(generate_links_header(name, bookmark))
        for i in range(COLCOUNT):
            result.append(generate_links_column(category['content'][i::COLCOUNT]))
        result.append(generate_links_footer())
    return '\n'.join(result) + '\n'


def generate_links_header(name, bookmark):
    return f'        <h2><a name="{bookmark}">{name}</a></h2>\n        <table border="0"><tr>'


def generate_links_column(content):
    result = ['          <td width="400" valign="top"><ul class="list-group">']
    for link in content:
        title, url, icon = extract_from_dict(link, 'name', 'url', 'icon')
        result.append(f'            <a class="list-group-item" href="{url}"><img src="icons/{icon}.png" class="img-rounded">&nbsp;{title}</a>')
    result.append('          </ul></td>')
    return '\n'.join(result)


def generate_links_footer():
    return '        </tr></table>'


def process_template(toc_section, links_section):
    with  open('index.html', 'w') as html_file:
        for line in open('template.html', 'r'):
            if line =='<!-- PLACEHOLDER: TABLE OF CONTENTS -->\n':
                html_file.write(toc_section)
            elif line == '<!-- PLACEHOLDER: LINK SECTIONS -->\n':
                html_file.write(links_section)
            else:
                html_file.write(line)

def extract_from_dict(dictionary, *keys):
    return [dictionary[key] for key in keys]


if __name__ == '__main__':
    main()
    print('processing complete')
