#!/usr/bin/python3.10

import json
import socket

COLCOUNT = 4


def main():
    print('INDEX.HTML')
    create('content.json', 'index.html', 'Bart\'s Internet Start Page')
    print('NOOKMARKS.HTML')
    create('bookmarks.json', 'bookmarks.html', 'Bookmarks')
    # create('work.json', 'work.html', 'Maersk startpage for the home')

def get_ip():
    '''Return ip address of this computer'''
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def create(input_name, output_name, title):
    try:
        data = read_content(input_name)
        toc_section = create_toc_code(data)
        links_section = create_links_code(data)
        process_template(output_name, title, toc_section, links_section)
    except json.decoder.JSONDecodeError as ex:
        print('The json file "{}" contains an error:'.format(input_name))
        print(ex)
    except Exception as ex:
        print('An error occured while processing:')
        print(type(ex))
        print(ex)



def read_content(name):
    '''
    Read the content from the json file and return it as a list of
    link categories, each with a list of individual links
    '''
    with open(name, 'r') as infile:
        return json.load(infile)


def create_toc_code(data):
    '''
    Create the html code for the table of contents
    (the panel on the left side)
    '''
    toc_section = ''
    for category in data:
        name, bookmark = extract_from_dict(category, 'name', 'bookmark')
        print('----\n  Name    : {name:12}\n  Bookmark: {bookmark}'.format(name=name, bookmark=bookmark))
        toc_section += '            <li><a href="#{bookmark}">{name}</a></li>\n'.format(bookmark=bookmark, name=name)
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
    return '        <h2><a name="{}">{}</a></h2>\n        <table border="0"><tr>'.format(bookmark, name)


def generate_links_column(content):
    local_ip = get_ip()
    result = ['          <td width="400" valign="top"><ul class="list-group">']
    for link in content:
        title, url, icon = extract_from_dict(link, 'name', 'url', 'icon')
        url = url.replace('localhost', local_ip)
        result.append('            <a class="list-group-item" href="{url}"><img src="icons/{icon}.png" class="img-rounded">&nbsp;{title}</a>'.format(url=url, icon=icon, title=title))
    result.append('          </ul></td>')
    return '\n'.join(result)


def generate_links_footer():
    return '        </tr></table>'


def process_template(name, title, toc_section, links_section):
    with  open(name, 'w') as html_file:
        for line in open('template.html', 'r'):
            if line == '    <title>TITLE</title>\n':
                html_file.write('    <title>{}</title>\n'.format(title))
            elif line =='<!-- PLACEHOLDER: TABLE OF CONTENTS -->\n':
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
