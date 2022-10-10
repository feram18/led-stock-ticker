from enum import Enum


class Status(Enum):
    """Update status enum class"""
    FAIL = 'FAIL'
    SUCCESS = 'SUCCESS'
    API_ERROR = 'API ERROR'
    NETWORK_ERROR = 'NETWORK ERROR'
