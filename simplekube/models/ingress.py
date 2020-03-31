import yaml

from kubernetes import client
from kubernetes.client import NetworkingV1beta1Ingress
from kubernetes.client.rest import ApiException

from simplekube.mixins import JinjaTemplateMixin
from simplekube.exceptions import SimpleApiException


class SimpleV1Ingress(NetworkingV1beta1Ingress, JinjaTemplateMixin):

    def __init__(self, api_client, name, issuer, host, paths=[], namespace='default'):
        self.api = client.NetworkingV1beta1Api(api_client)
        self.name = name
        self.namespace = namespace

        self._issuer = issuer
        self._host = host
        self._paths = paths

        context = {
            'name': name,
            'issuer': issuer,
            'host': host,
            'paths': paths,
        }

        config = yaml.safe_load(self.generate_template('ingress.yaml.j2', context))
        NetworkingV1beta1Ingress.__init__(self, api_version=config['apiVersion'], kind=config['kind'], metadata=config['metadata'], spec=config['spec'], status=None)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host
        # TODO: update host
        # self._spec['rules'][0]['host'] = host
        # self._spec['tls'][0]['hosts'][0][] = host

    @property
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, paths):
        self._paths = paths
        context = {
            'name': self.name,
            'host': self.host,
            'paths': paths,
        }
        config = yaml.safe_load(self.generate_template('ingress.yaml.j2', context))
        self._spec = config['spec']

    def create(self, pretty=False):
        try:
            return self.api.create_namespaced_ingress(self.namespace, self.to_dict(), pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)

    def delete(self, pretty=False, grace_period_seconds=0, propagation_policy='Foreground'):
        try:
            return self.api.delete_namespaced_ingress(self.name, self.namespace, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy, pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)

    def read(self, pretty=False):
        try:
            return self.api.read_namespaced_ingress(self.name, self.namespace, pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)

    def patch(self, pretty=False):
        try:
            return self.api.patch_namespaced_ingress(self.name, self.namespace, self.to_dict(), pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)
