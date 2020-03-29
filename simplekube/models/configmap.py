import yaml

from kubernetes.client import V1ConfigMap
from kubernetes.client.rest import ApiException

from mixins import JinjaTemplateMixin


class SimpleV1ConfigMap(V1ConfigMap, JinjaTemplateMixin):

    def __init__(self, api, name, variables=[], namespace='default'):
        self.api = api
        self.name = name
        self.namespace = namespace
        self._variables = variables

        context = {
            'name': name,
            'variables': variables
        }

        config = yaml.safe_load(self.generate_template('configmap.yaml.j2', context))
        V1ConfigMap.__init__(self, api_version=config['apiVersion'], kind=config['kind'], metadata=config['metadata'], data=config['data'])

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables):
        self._variables = variables
        config = yaml.safe_load(self.generate_template('configmap.yaml.j2', {'variables': variables}))
        self._data = config['data']

    def create(self, pretty=False):
        try:
            api_response = self.api.create_namespaced_config_map(self.namespace, self.to_dict(), pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

    def delete(self, pretty=False, grace_period_seconds=0, propagation_policy='Foreground'):
        try:
            api_response = self.api.delete_namespaced_config_map(self.name, self.namespace, pretty=pretty, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_config_map: %s\n" % e)

    def patch(self, pretty=False):
        try:
            api_response = self.api.patch_namespaced_config_map(self.name, self.namespace, self.to_dict(), pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->patch_namespaced_config_map: %s\n" % e)

    def read(self, pretty=False):
        try:
            api_response = self.api.read_namespaced_config_map(self.name, self.namespace, pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_config_map: %s\n" % e)
