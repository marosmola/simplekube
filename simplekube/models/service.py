import yaml

from kubernetes.client import V1Service
from kubernetes.client.rest import ApiException

from simplekube.mixins import JinjaTemplateMixin
from simplekube.exceptions import SimpleApiException


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

        config = yaml.safe_load(self.generate_template('service.yaml.j2', context))
        V1Service.__init__(self, api_version=config['apiVersion'], kind=config['kind'], metadata=config['metadata'], spec=config['spec'], status=None)

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
            return self.api.create_namespaced_service(self.namespace, self.to_dict(), pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)

    def delete(self, pretty=False, grace_period_seconds=0, propagation_policy='Foreground'):
        try:
            return self.api.delete_namespaced_service(self.name, self.namespace, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy, pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)

    def read(self, pretty=False):
        try:
            return self.api.read_namespaced_service(self.name, self.namespace, pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)

    def patch(self, force=False, pretty=False):
        try:
            return self.api.patch_namespaced_service(self.name, self.namespace, self.to_dict(), pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)
