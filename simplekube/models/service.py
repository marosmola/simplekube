import yaml

from kubernetes import client
from kubernetes.client import V1Service
from kubernetes.client.rest import ApiException

from mixins import JinjaTemplateMixin

class SimpleV1Service(V1Service, JinjaTemplateMixin):

    def __init__(self, api, name, app, port, namespace='default'):
        self.api = api
        self.name = name
        self.namespace = namespace
        self._app = app
        self._port = port

        context = {
            'name': name,
            'app': app,
            'port': port
        }

        config = yaml.safe_load(self.generate_template('configmap.yaml.j2', context))
        V1Service.__init__(api_version=config['apiVersion'], kind=config['kind'], metadata=config['metadata'], spec=config['spec'], status=None)

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        self._app = app
        self._metadata['labels']['app'] = app
        self._spec['selector']['app'] = app

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port
        self._spec['ports'][0]['targetPort'] = port

    def create(self, pretty=False):
        try:
            api_response = self.api.create_namespaced_service(self.namespace, self.to_dict(), pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)

    def delete(self, pretty=False, grace_period_seconds=0, propagation_policy='Foreground'):
        try:
            api_response = self.api.delete_namespaced_service(self.name, self.namespace, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy, pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)

    def read(self, pretty=False):
        try:
            api_response = self.api.read_namespaced_service(self.name, self.namespace, pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_service: %s\n" % e)

    def patch(self, force=False, pretty=False):
        # TODO: force: Forbidden: may not be specified for non-apply patch
        try:
            api_response = self.api.patch_namespaced_service(self.name, self.namespace, self.to_dict(), pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->patch_namespaced_service: %s\n" % e)
