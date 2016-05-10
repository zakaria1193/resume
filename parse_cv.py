import os,sys
import logging
import yaml

class BuildCV(object):
    """Parse YAML config file, print a markdown file and a tex file"""

    def __init__(self,data_file, md_out_file=None, tex_out_file=None,moderncv_tex_header_template=None):
        """Constructor"""
        self.tex_out_file = tex_out_file
        self.md_out_file = md_out_file
        self.moderncv_tex_header_template = moderncv_tex_header_template
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.info('Reading CV data from %s'%data_file)
        with open(data_file,'r') as f:
            self.yaml_obj = yaml.load(f)

    def _write_cv_item(self,iterator,key_a,key_b):
        """write list to \cvitem tex object"""
        cvitem_temp = '\cvitem{%s}{%s}\n'
        cvitem_string =''
        for item in iterator:
            cvitem_string += cvitem_temp%(item[key_a],item[key_b])
        cvitem_string += '%\n'
        return cvitem_string

    def _write_cv_item_list(self,iterator):
        """write list to \cvitemlist tex object"""
        cvitem_list_temp = '\cvitemlist{%s}\n'
        cvitem_list_string = ''
        for item in iterator:
            cvitem_list_string += cvitem_list_temp%(item)
        cvitem_list_string += '%\n'
        return cvitem_list_string

    def _format_pub(self,pub_entry):
        """Format string of publication info"""
        if pub_entry['url'] and pub_entry['doi']:
            return '%s, \\textit{%s}, %s, %s, \href{%s}{%s}'%(pub_entry['authors'], pub_entry['title'], pub_entry['journal'], pub_entry['year'], pub_entry['url'], pub_entry['doi'])
        else:
            return '%s, \\textit{%s}, %s, %s'%(pub_entry['authors'], pub_entry['title'], pub_entry['journal'], pub_entry['year'])

    def _configure_tex_header(self,f,color,style):
        """Write TeX header"""
        if not self.moderncv_tex_header_template:
            raise ValueError('Missing TeX header filename.')

        self.logger.info('Configuring header from %s'%(self.moderncv_tex_header_template))
        pa = self.yaml_obj['preamble']
        with open(self.moderncv_tex_header_template,'r') as g:
            tex_header = ''.join(g.readlines())
        f.write(tex_header%(color,style,pa['name']['first'], pa['name']['last'], pa['address']['street'], pa['address']['city'], pa['address']['country'], pa['contact']['phone'], pa['contact']['mail'], pa['contact']['github'], pa['name']['first']+' '+pa['name']['last'],'CV','CV typeset with ModernCV class'))

    def write_tex(self,moderncv_color='black',moderncv_style='banking'):
        """Write CV to LaTeX file using moderncv class"""
        if not self.tex_out_file:
            raise ValueError('Specify TeX file to write to first.')

        self.logger.info('Writing TeX file to %s'%(self.tex_out_file))
        self.logger.info('Using style: %s'%(moderncv_style))
        self.logger.info('Using color: %s'%(moderncv_color))
        #open file
        f = open(self.tex_out_file,'w')
        #write header
        self._configure_tex_header(f,moderncv_color,moderncv_style)
        #open body
        f.write('\\begin{document}\n')
        f.write('\makecvtitle\n')
        #alias section dictionary
        sections = self.yaml_obj['sections']
        #personal
        f.write('\section{%s}\n'%(sections['personal_information']['title']))
        f.write(self._write_cv_item(sections['personal_information']['items'],'name','value'))
        #computing
        f.write('\section{%s}\n'%(sections['computing']['title']))
        f.write(self._write_cv_item(sections['computing']['items'],'name','value'))
        #publications
        f.write('\section{%s}\n'%(sections['publications']['title']))
        f.write(self._write_cv_item_list([self._format_pub(entry) for entry in sections['publications']['entries']]))
        #close body
        f.write('\end{document}')
        #close file
        f.close()

    def write_markdown(self):
        """Write CV to markdown"""
        if not self.md_out_file:
            raise ValueError('Specify Markdown file to write to first.')

        self.logger.info('Writing Markdown file to %s'%(self.md_out_file))
        f = open(self.md_out_file,'w')
        #Education
        f.write('## %s\n'%(self.yaml_obj['sections']['education']['title']))
        f.write('\n')
        for school in self.yaml_obj['sections']['education']['entries']:
            school_string = '* %s, %s / %s'%(school['degree'], school['dates'] ,school['school'])
            if school['items']:
                school_string += ' / %s'%(' / '.join(school['items']))
            f.write(school_string+'\n')
        f.write('\n')
        #Skills
        f.write('## %s\n'%(self.yaml_obj['sections']['computing']['title']))
        f.write('\n')
        for item in self.yaml_obj['sections']['computing']['items']:
            f.write('* **%s**: %s\n'%(item['name'],item['value']))
        f.write('\n')
        #Presentations
        f.write('## %s\n'%(self.yaml_obj['sections']['presentations']['title']))
        f.write('\n')
        for pres in self.yaml_obj['sections']['presentations']['entries']:
            if pres['url']:
                pres_string = '* %s: [*%s*](%s) / %s / %s / %s / %s\n'%(pres['type'], pres['title'], pres['url'], pres['event'], pres['institution'], pres['location'], pres['date'])
            else:
                pres_string = '* %s: *%s* / %s / %s / %s / %s\n'%(pres['type'], pres['title'], pres['event'], pres['institution'], pres['location'], pres['date'])
            f.write(pres_string)
        f.write('\n')
        #Publications
        f.write('## %s\n'%(self.yaml_obj['sections']['publications']['title']))
        f.write('\n')
        for pub in self.yaml_obj['sections']['publications']['entries']:
            f.write('* %s, *%s*, %s, %s\n'%(pub['authors'], pub['title'], pub['journal'], pub['year']))
        f.write('\n')
        #close the file
        f.close()

if __name__=='__main__':
    cv_builder = BuildCV('cv_data.yml', md_out_file='test_md_cv.md', moderncv_tex_header_template='moderncv_tex_header.tex', tex_out_file='test_tex_cv.tex')
    cv_builder.write_markdown()
    cv_builder.write_tex()
