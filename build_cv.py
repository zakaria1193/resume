import os
import sys
import argparse
import logging

import yaml
import jinja2

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import filters


class BuildCV(object):
    """
    Build markdown and tex files of CV from YAML using jinja templates
    """

    def __init__(self, yaml_config_file, md_template=None, tex_template=None, filters=None):
        self.tex_template = tex_template
        self.md_template = md_template
        self.filters = filters
        with open(yaml_config_file, 'r') as f:
            self.yaml_obj = yaml.load(f)

    @property
    def jenv_md(self,):
        """
        Set up markdown/HTML environment
        """
        jenv_md = jinja2.Environment(loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')))
        for f in self.filters:
            jenv_md.filters[f.__name__] = f
        return jenv_md

    @property
    def jenv_tex(self,):
        """
        Set up TeX environment
        """
        jenv_tex = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')))
        # define new delimiters to avoid TeX conflicts
        jenv_tex.block_start_string = '((*'
        jenv_tex.block_end_string = '*))'
        jenv_tex.variable_start_string = '((('
        jenv_tex.variable_end_string = ')))'
        jenv_tex.comment_start_string = '((='
        jenv_tex.comment_end_string = '=))'
        for f in self.filters:
            jenv_tex.filters[f.__name__] = f
        return jenv_tex

    def write_tex_cv(self, out_file, moderncv_color='black', moderncv_style='banking'):
        """Write TeX CV with jinja template"""
        template = self.jenv_tex.get_template(self.tex_template)
        with open(out_file, 'w') as f:
            f.write(template.render(moderncv_color=moderncv_color,
                                    moderncv_style=moderncv_style, db=self.yaml_obj))

    def write_md_cv(self, out_file, pdf_link=None):
        """Write markdown/HTML CV with jinja template"""
        template = self.jenv_md.get_template(self.md_template)
        with open(out_file, 'w') as f:
            f.write(template.render(db=self.yaml_obj, pdf_link=pdf_link))


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Build TeX and Markdown versions of your CV')
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    parser.add_argument("--cv_data", help="YAML config file containing all CV data",
                        default=os.path.join(cur_dir, 'cv_data.yml'))
    parser.add_argument("--md_template", help="Markdown/HTML template")
    parser.add_argument("--tex_template", help="TeX template")
    parser.add_argument("--md_out_file", help="where to write tex version of CV to")
    parser.add_argument("--tex_out_file", help="where to write markdown version of CV to")
    parser.add_argument("--pdf_link", help="where to link to PDF version of CV")
    args = parser.parse_args()
    # build cv
    filters = [filters.escape_tex, filters.tex_section_sorter, filters.tex_pub_sorter,
               filters.md_section_sorter, filters.html_section_sorter, filters.shorten_list]
    cv_builder = BuildCV(args.cv_data, md_template=args.md_template, tex_template=args.tex_template,
                         filters=filters)
    if args.tex_out_file is not None:
        cv_builder.write_tex_cv(args.tex_out_file)
    if args.md_out_file is not None:
        cv_builder.write_md_cv(args.md_out_file, pdf_link=args.pdf_link)
