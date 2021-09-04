"""Update status enum class"""
from enum import Enum


class Status(Enum):
    FAIL = 'FAIL'
    SUCCESS = 'SUCCESS'
    API_ERROR = 'API ERROR'
    NETWORK_ERROR = 'NETWORK ERROR'
