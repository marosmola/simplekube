import yaml
from pprint import pprint

from kubernetes import client
from kubernetes.client import V1Deployment
from kubernetes.client.rest import ApiException

from simplekube.mixins import JinjaTemplateMixin
from simplekube.exceptions import SimpleApiException


class SimpleV1Deployment(V1Deployment, JinjaTemplateMixin):

    def __init__(self, api, name, app, image, version, port, configmap=None, args=[], secret=None, replicas=1, namespace='default'):
        self.api = api
        self.name = name
        self.namespace = namespace

        self._app = app
        self._image = image
        self._version = version

        # TODO: set as properties
        self._port = port
        self._configmap = configmap
        self._args = args
        self._secret = secret
        self._replicas = replicas

        context = {
            'name': name,
            'app': app,
            'replicas': replicas,
            'image': image,
            'version': version,
            'port': port,
            'args': args,
            'configmap': configmap,
            'secret': secret
        }

        config = yaml.safe_load(self.generate_template('deployment.yaml.j2', context))
        V1Deployment.__init__(self, api_version=config['apiVersion'], kind=config['kind'], metadata=config['metadata'], spec=config['spec'], status=None)

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        self._app = app
        self._metadata['labels']['app'] = app
        self._spec['selector']['matchLabels']['app'] = app
        self._spec['template']['metadata']['labels']['app'] = app

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        self._spec['template']['spec']['containers'][0]['image'] = '{}:{}'.format(image, self.version)

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version
        self._spec['template']['spec']['containers'][0]['image'] = '{}:{}'.format(self.image, version)

    @property
    def replicas(self):
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        self._replicas = replicas
        self._spec['replicas'] = replicas

    def create(self, pretty=False):
        try:
            return self.api.create_namespaced_deployment(self.namespace, self.to_dict(), pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)

    def delete(self, pretty=False, grace_period_seconds=0, propagation_policy='Foreground'):
        try:
            return self.api.delete_namespaced_deployment(self.name, self.namespace, pretty=pretty, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy)
        except ApiException as e:
            raise SimpleApiException(e)

    def patch(self, pretty=False):
        try:
            return self.api.patch_namespaced_deployment(self.name, self.namespace, self.to_dict(), pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)
