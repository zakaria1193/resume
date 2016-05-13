import os,sys
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
        #set up environment
        self.jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates')))
        #define new delimiters to avoid TeX conflicts
        self.jenv.block_start_string = '((*'
        self.jenv.block_end_string = '*))'
        self.jenv.variable_start_string = '((('
        self.jenv.variable_end_string = ')))'
        self.jenv.comment_start_string = '((='
        self.jenv.comment_end_string = '=))'
        for f in filters:
            self.jenv.filters[f.__name__] = f

    def write_tex_cv(self,moderncv_color='black',moderncv_style='banking'):
        """Write TeX CV with jinja template"""
        template = self.jenv.get_template(self.tex_template)
        with open(self.tex_out_file,'w') as f:
            f.write(template.render(moderncv_color=moderncv_color, moderncv_style=moderncv_style, db=self.yaml_obj))

    def write_md_cv(self):
        """Write markdown CV with jinja template"""

if __name__=='__main__':
    cv_builder = BuildCV('cv_data.yml', md_out_file='test_md_cv.md', tex_out_file='test_tex_cv.tex')
    cv_builder.config_jinja_env(filters=[filters.escape_tex, filters.tex_section_sorter, filters.tex_pub_sorter])
    cv_builder.write_tex_cv()
