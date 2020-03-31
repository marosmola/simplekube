import os

from jinja2 import Environment, FileSystemLoader


class JinjaTemplateMixin(object):

    def generate_template(self, template, context):
        dir_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__))),
            'templates')
        env = Environment(loader=FileSystemLoader(dir_path))
        return env.get_template(template).render(object=context)
