import json

from kubernetes.client.rest import ApiException


class SimpleApiException(Exception):
    def __init__(self, api_exception):
        self.status = api_exception.status
        self.reason = api_exception.reason
        self.body = api_exception.body
        self.headers  = api_exception.headers

    def format_body(self):
        if self.body:
            return json.loads(self.body)
        return None

    def __str__(self):
        body = self.format_body()
        if body:
            error_message = "{}:{}".format(body['reason'], body['message'])
        else:
            error_message = "{}:{}".format(self.status, self.reason)
        return error_message
