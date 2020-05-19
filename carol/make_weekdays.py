SPACE = ' ' * 10

def main():
    text = [
        '<html>',
        '  <head>',
        '    <title>Carol\'s Weekdays</title>',
        '    <style>',
        '      table, th, td {',
        '      border-collapse: collapse;}',
        '    </style>',
        '  </head>',
        '  <body>',
        *create_cell(sun(), cloud()),
        *create_cell(calendar('Monday'), calendar('Tuesday')),
        *create_cell(calendar('Tuesday'), calendar('Wednesday')),
        *create_cell(calendar('Wednesday'), calendar('Thursday')),
        *create_cell(calendar('Thursday'), calendar('Friday')),
        *create_cell(calendar('Friday'), calendar('Saturday')),
        '  </body>',
        '</html>',
    ]
    with open('weekdays.html', 'w') as f:
        for t in text:
            f.write(t + '\n')

def create_cell(left='&nbsp;', right='&nbsp;'):
    return [
        '    <table border="0" width="1200" height="700" align="center">',
        '      <tr>',
        '        <td width="700" align="center">',
        left,
        '        </td>',
        '        <td width="700", align="center">',
        right,
        '        </td>',
        '      </tr>',
        '    </table><br><br><br><br><br>'
    ]


def sun():
    return SPACE + '<img src="sun.png" width="500">'


def cloud():
    return SPACE + '<img src="cloud.png" width="500">'


def calendar(title='Calendar'):
    # border around calendar
    text = SPACE
    text += '<table border="2" width="500 height="500" align="center">'
    text += '<tr><td align="center" valign="middle">'
    text += '<br><br><br><h1>' + title + '<h1>'
    text += '<table width="300" align="center" border="2"'
    text += '<tr>'
    for r in range(6):
        tag = 'th' if r == 0 else 'td'
        for day in 'Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa':
            disp_day = day if r == 0 else '&nbsp;'
            if day.casefold() == title.casefold()[:2]:
                text += f'<{tag} width="14.3%" bgcolor="yellow">{disp_day}</{tag}>'
            else:
                text += f'<{tag} width="14.3%">{disp_day}</{tag}>'
        text += '</tr>'
    text += '</table><br><br><br>'
    text += '</td></tr>'
    text += '</table>'
    return text


if __name__ == '__main__':
    main()