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
            error_message = {
                'status_code': self.status,
                'reason': body['reason'],
                'message': body['message'],
            }
        else:
            error_message = {
                'status_code': self.status,
                'reason': self.reason,
                'message': "",
            }
        return str(error_message)
