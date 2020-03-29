from kubernetes import client
from kubernetes.client.rest import ApiException


class MyV1Service(client.V1Service):

    def __init__(self, api, name, app, port, namespace='default'):
        """
        Docs to be added
        """
        self.api = api
        self.name = name
        self.namespace = namespace

        self._app = app
        self._port = port

        metadata = {
            "labels": {
                "app": app
            },
            "name": name
        }

        spec = {
            "ports": [
                {
                    "name": "api",
                    "port": 80,
                    "protocol": "TCP",
                    "targetPort": port
                }
            ],
            "selector": {
                "app": app
            }
        }
        super().__init__(api_version='v1', kind='Service', metadata=metadata, spec=spec, status=None)

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
