"""
    Models for easy access to kube API
"""

from .deployment import SimpleV1Deployment
from .namespace import SimpleV1Namespace
from .service import SimpleV1Service
from .configmap import SimpleV1ConfigMap
from .secret import SimpleV1Secret
from .ingress import SimpleV1Ingress
