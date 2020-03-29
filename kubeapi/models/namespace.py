from kubernetes import client
from kubernetes.client.rest import ApiException


class MyV1Namespace(client.V1Namespace):

    def __init__(self, api, name):
        self.api = api
        self.name = name
        metadata = {
            'name': name
        }
        super().__init__(api_version='v1', kind='Namespace', metadata=metadata, spec=None, status=None)

    def create(self, pretty=False):
        try:
            api_response = self.api.create_namespace(self.to_dict(), pretty=pretty)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespace: %s\n" % e)

    def delete(self, pretty=False, grace_period_seconds=0, propagation_policy='Foreground'):
        try:
            api_response = self.api.delete_namespace(self.name, pretty=pretty, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespace: %s\n" % e)
