from kubernetes import client
from kubernetes.client.rest import ApiException

from simplekube.exceptions import SimpleApiException

class SimpleV1Namespace(client.V1Namespace):

    def __init__(self, api, name):
        self.api = api
        self.name = name
        metadata = {
            'name': name
        }
        super().__init__(api_version='v1', kind='Namespace', metadata=metadata, spec=None, status=None)

    def create(self, pretty=False):
        try:
            return self.api.create_namespace(self.to_dict(), pretty=pretty)
        except ApiException as e:
            raise SimpleApiException(e)

    def delete(self, pretty=False, grace_period_seconds=0, propagation_policy='Foreground'):
        try:
            return self.api.delete_namespace(self.name, pretty=pretty, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy)
        except ApiException as e:
            raise SimpleApiException(e)
