import yaml

from kubernetes import client
from kubernetes.client import V1Secret
from kubernetes.client.rest import ApiException

from mixins import JinjaTemplateMixin


class SimpleV1Secret(V1Secret, JinjaTemplateMixin):

    def __init__(self, api, name, secret_type, variables=[], namespace='default'):
        self.api = api
        self.name = name
        self.namespace = namespace

        self._secret_type = secret_type
        self._variables = variables

        context = {
            'name': name,
            'type': secret_type,
            'variables': variables
        }

        config = yaml.safe_load(self.generate_template('secret.yaml.j2', context))
        V1Secret.__init__(self, api_version=config['apiVersion'], kind=config['kind'], metadata=config['metadata'], data=config['data'], type=config['type'])

    @property
    def secret_type(self):
        return self._secret_type

    @secret_type.setter
    def secret_type(self, secret_type):
        self._secret_type = secret_type
        self._type = secret_type

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
            api_response = self.api.create_namespaced_secret(self.namespace, self.to_dict(), pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

    def delete(self, pretty=False, grace_period_seconds=0, propagation_policy='Foreground'):
        try:
            api_response = self.api.delete_namespaced_secret(self.name, self.namespace, pretty=pretty, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_config_map: %s\n" % e)

    def patch(self, pretty=False):
        try:
            api_response = self.api.patch_namespaced_secret(self.name, self.namespace, self.to_dict(), pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->patch_namespaced_config_map: %s\n" % e)

    def read(self, pretty=False):
        try:
            api_response = self.api.read_namespaced_secret(self.name, self.namespace, pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_config_map: %s\n" % e)
