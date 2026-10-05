"""
Connector registry package.
"""

from .base import BaseConnector
from .drive_connector import DriveConnector
from .email_connector import EmailConnector
from .erp_connector import ERPConnector
from .registry_connector import RegistryConnector


def get_default_connectors():
    return [
        DriveConnector(),
        EmailConnector(),
        ERPConnector(),
        RegistryConnector(),
    ]


__all__ = [
    "BaseConnector",
    "DriveConnector",
    "EmailConnector",
    "ERPConnector",
    "RegistryConnector",
    "get_default_connectors",
]
