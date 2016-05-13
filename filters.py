#name:filters.py
#author: Will Barnes
#date created: 12 May 2016
#description: filters for printing TeX to jinja templates. See See http://flask.pocoo.org/snippets/55/ for more info.

import re
import logging

LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

def tex_section_sorter(section,title,index):
    """Change format based on section. Customized for my specific setup"""
    cv_listitem_format = '\cvlistitem{%s}'
    if title=='Education':
        return_list =  [section['dates'], section['degree'], section['school'], section['location'], section['gpa'] if section['gpa'] else '','']
        if section['cvlistitems']:
            return_list[-1] = '\n'.join([cv_listitem_format%(i) for i in section['cvlistitems']])
    elif title=='Talks and Posters':
        return_list = [section['dates'], section['institution'], section['event'], section['location'],'',section['type']+' title: '+'\\textit{%s}'%(section['title'])]
        if section['url']:
            return_list[-1] = section['type']+' title: ' + '\href{%s}{%s}'%(section['url'],'\\textit{%s}'%(section['title']))
    elif title=='Research Positions':
        return_list = [section['dates'], section['title'], section['institution'], section['location'],'',section['description']]
    elif title=='Teaching Experience':
        return_list = [section['dates'], section['title'], section['class'], '', '', section['description']]
    elif title=='Societies and Associations' or title=='Employment Experience':
        return_list = [section['dates'], section['title'], section['org'], '', '', section['description']]
    else:
        logging.error('Unrecognized title: %s'%(title))

    return return_list[index]

def tex_pub_sorter(entry):
    """Format publication list item"""
    if entry['doi'] and entry['url']:
        return '%s, \\textit{%s}, %s, %s, \href{%s}{%s}'%(entry['authors'], entry['title'], entry['journal'], entry['year'], entry['url'], entry['doi'])
    else:
        return '%s, \\textit{%s}, %s, %s'%(entry['authors'], entry['title'], entry['journal'], entry['year'])

def md_section_sorter(entry,title):
    """Format markdown sections for different types"""
    if title == 'Education':
        return_str = '%s, %s / %s '%(entry['degree'], entry['dates'], entry['school'])
        if entry['cvlistitems']:
            return_str += ' / ' + ' / '.join([item for item in entry['cvlistitems']])
    elif title == 'Talks and Posters':
        if entry['url']:
            return_str = '%s: [*%s*](%s) / %s / %s / %s / %s'%(entry['type'], entry['title'], entry['url'], entry['event'], entry['institution'], entry['location'], entry['dates'])
        else:
            return_str = '%s: *%s* / %s / %s / %s / %s'%(entry['type'], entry['title'], entry['event'], entry['institution'], entry['location'], entry['dates'])
    elif title == 'Publications':
        return_str = '%s, *%s*, %s, %s'%(entry['authors'], entry['title'], entry['journal'], entry['year'])
        if entry['url'] and entry['doi']:
            return_str += ', [%s](%s)'%(entry['doi'],entry['url'])
    else:
        logger.error('Unrecognized title: %s'%(title))

    return return_str
