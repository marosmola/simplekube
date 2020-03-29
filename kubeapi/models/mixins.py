import os

from jinja2 import Environment, FileSystemLoader


class JinjaTemplateMixin(object):

    def generate_template(self, template, context):
        env = Environment(loader=FileSystemLoader('/home/maro/Projects/django-devops/kubeapi/templates/'))
        return env.get_template(template).render(object=context)
