from collections import namedtuple

import requests
from pydantic import BaseModel

from ...domain.identifier_handler import IdentifierAlgorithm, IdentifierHandler

UserId = namedtuple("UserIdentifier", "value")


class UserServer(BaseModel):
    url: str


class UserService:
    algorithm = IdentifierAlgorithm.UUID_V4
    pk = "userId"

    def __init__(self, ref_user_service: UserServer):
        self.user_client = ref_user_service

    def is_valid_user_id(self, userId):
        payload = {"userId": userId}
        r = requests.get(self.user_client.url, params=payload)
        return True if r.status_code == 200 else False

    @classmethod
    def get_default_identifier(cls):
        return UserId(IdentifierHandler.get_default_identifier(cls.algorithm))

    @classmethod
    def set_identifier(cls, identifier):
        IdentifierHandler.is_valid(cls.algorithm, identifier)
        return UserId(identifier)
