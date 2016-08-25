import os,sys
import argparse
import logging
import yaml
import jinja2
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import filters

class BuildCV(object):
    """Build markdown and tex files of CV from YAML using jinja templates"""

    def __init__(self, yaml_config_file, md_template='cv_template.md', tex_template='cv_template.tex', md_out_file=None, tex_out_file=None):
        """Constructor"""
        self.tex_out_file = tex_out_file
        self.md_out_file = md_out_file
        self.tex_template = tex_template
        self.md_template = md_template
        self.logger = logging.getLogger(type(self).__name__)
        #read in yaml config file
        self.logger.info('Reading CV data from %s'%yaml_config_file)
        with open(yaml_config_file,'r') as f:
            self.yaml_obj = yaml.load(f)

    def config_jinja_env(self,filters=[]):
        """Setup jinja environment. """
        #set up markdown environment
        self.jenv_md = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates')))
        for f in filters:
            self.jenv_md.filters[f.__name__] = f
        #set up tex environment
        self.jenv_tex = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates')))
        #define new delimiters to avoid TeX conflicts
        self.jenv_tex.block_start_string = '((*'
        self.jenv_tex.block_end_string = '*))'
        self.jenv_tex.variable_start_string = '((('
        self.jenv_tex.variable_end_string = ')))'
        self.jenv_tex.comment_start_string = '((='
        self.jenv_tex.comment_end_string = '=))'
        for f in filters:
            self.jenv_tex.filters[f.__name__] = f

    def write_tex_cv(self,moderncv_color='black',moderncv_style='banking'):
        """Write TeX CV with jinja template"""
        template = self.jenv_tex.get_template(self.tex_template)
        with open(self.tex_out_file,'w') as f:
            f.write(template.render(moderncv_color=moderncv_color, moderncv_style=moderncv_style, db=self.yaml_obj))

    def write_md_cv(self,pdf_link=None):
        """Write markdown CV with jinja template"""
        template = self.jenv_md.get_template(self.md_template)
        with open(self.md_out_file,'w') as f:
            f.write(template.render(db=self.yaml_obj,pdf_link=pdf_link))


if __name__=='__main__':
    #parse command line arguments
    parser = argparse.ArgumentParser(description='Build TeX and Markdown versions of your CV')
    parser.add_argument("--cv_data",help="YAML config file containing all CV data", default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'cv_data.yml'))
    parser.add_argument("--md_out_file",help="where to write tex version of CV to", default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'output','cv.md'))
    parser.add_argument("--tex_out_file",help="where to write markdown version of CV to",default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'output','cv.tex'))
    parser.add_argument("--pdf_link",help="where to link to PDF version of CV")
    args = parser.parse_args()
    #build cv
    cv_builder = BuildCV(args.cv_data, md_out_file=args.md_out_file, tex_out_file=args.tex_out_file)
    cv_builder.config_jinja_env(filters=[filters.escape_tex, filters.tex_section_sorter, filters.tex_pub_sorter, filters.md_section_sorter])
    cv_builder.write_tex_cv()
    cv_builder.write_md_cv(pdf_link=args.pdf_link)
