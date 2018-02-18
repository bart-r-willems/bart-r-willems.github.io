#!python3

import xml.etree.ElementTree as ET
import math

COLCOUNT = 4

class Category(object):
    def __init__(self, name, bookmark):
        self.name = name
        self.bookmark = bookmark
        self.itemlist = []

    def item_column(self, col_num, colcount):
        """return a column with x subitems based on column number and column count"""
        col_size = int(math.ceil(float(len(self.itemlist)) / colcount))
        result = []
        for i in range(col_num, len(self.itemlist), colcount):
            result.append(self.itemlist[i])
        return result
        # return self.itemlist[col_num * col_size: min((col_num + 1) * col_size, len(self.itemlist) + 1)]

def main():
    toc_section = ''
    links_section = ''
    toc = read_toc()
    for category in toc:
        print('----\n  Name    : {:}\n  Bookmark: {:}'.format(category.name, category.bookmark))
        toc_section += '            <li><a href="#{:}">{:}</a></li>\n'.format(category.bookmark, category.name)
        links_section += '        <h2><a name="{:}">{:}</a></h2>\n'.format(category.bookmark, category.name)
        links_section += '          <table border="0"><tr>\n'
        # cycle through all link columns
        for i in range(COLCOUNT):
            links_section += '        <td width="400" valign="top"><ul class="list-group">\n'
            for link in category.item_column(i, COLCOUNT):
                links_section += '            <a class="list-group-item" href="{:}"><img src="icons/{:}.png" class="img-rounded">&nbsp;{:}</a>\n'.format(link[1], link[2], link[0])
            links_section += '        </ul></td>\n'
        links_section += '          </tr></table>\n'

    template_file = open('template.html', 'r')
    html_file = open('index.html', 'w')
    for line in template_file:
        if line =='<!-- PLACEHOLDER: TABLE OF CONTENTS -->\n':
            html_file.write(toc_section)
        elif line == '<!-- PLACEHOLDER: LINK SECTIONS -->\n':
            html_file.write(links_section)
        else:
            html_file.write(line)

    template_file.close()
    html_file.close()

def read_toc():
    result = []
    tree = ET.parse('contents.xml')
    root = tree.getroot()
    for category in root:
        if category.tag == 'category':
            catlist = Category(category.attrib['name'], category.attrib['bookmark'])
            for link in category:
                if link.tag == 'link':
                    if 'icon' not in link.attrib:
                        catlist.itemlist.append((link.attrib['name'], link.attrib['url'], 'default'))
                    else:
                        catlist.itemlist.append((link.attrib['name'], link.attrib['url'], link.attrib['icon']))
            result.append(catlist)
    return result

if __name__ == '__main__':
    main()
    print('processing complete')
