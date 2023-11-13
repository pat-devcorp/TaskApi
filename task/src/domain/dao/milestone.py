from enum import Enum
from typing import Tuple

from validator_collection import checkers

from ...utils.DatetimeHandler import valdiateDateFormat
from ...utils.IdentityHandler import IdentityAlgorithm, IdentityHandler
from ..DomainError import DomainError


class MemberRole(Enum):
    MEMBER: 0


class Milestone:
    @staticmethod
    def getFields() -> list:
        return ["milestone_id", "description"]

    @classmethod
    def getMock():
        return {"milestone_id": 0, "description": "Test"}

    @classmethod
    def filterKeys(cls, params: dict, is_partial=True) -> dict:
        if is_partial:
            return {
                k: v
                for k, v in params.items()
                if k in cls.getFields() and v is not None
            }
        if params.keys() != cls.getFields():
            raise DomainError("Fail to create meeting")
        data = dict()
        for k in cls.getFields():
            if params.get(k) is None:
                raise DomainError(f"{k}: must be present in meeting")
            data[k] = params[k]
        return data

    @classmethod
    def isValid(cls, ref_object: dict) -> str:
        print("---DOMAIN---")
        print(ref_object)
        validate_funcs = {
            "milestone_id": cls.isValidIdentifier,
            "description": cls.validateDescription,
        }

        meeting = {k: v for k, v in ref_object.items() if k in validate_funcs.keys()}

        errors = list()
        for k, v in meeting.items():
            func = isValid_funcs[k]
            is_ok, err = func(v)
            if not is_ok:
                errors.append(err)

        if len(errors) > 0:
            return "\n".join(errors)

        return None

    @staticmethod
    def isValidIdentifier(ticket_id: str) -> Tuple[bool, str]:
        if not IdentityHandler.isValid(ticket_id, IdentityAlgorithm.DEFAULT):
            return False, "Identity not valid for meeting"
        return True, ""

    @staticmethod
    def isValidDescription(description: str) -> Tuple[bool, str]:
        if not checkers.is_string(description, maximum_lengt=200):
            return False, "Max length exceeded, not allowed"
        return True, ""