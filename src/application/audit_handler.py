from ..domain.identifier_handler import IdentifierAlgorithm, IdentifierHandler
from ..infrastructure.services.User import UserService
from ..utils.custom_date import CustomDatetime
from ..utils.HandlerError import HandlerError
from ..utils.status_code import ID_NOT_FOUND, SCHEMA_NOT_MATCH, WRITER_NOT_FOUND


class AuditHandler:
    _fields = ["writeUId", "writeAt", "createUId", "createAt", "endAt"]

    @staticmethod
    def get_mock() -> dict:
        now = CustomDatetime.str_now()
        return {
            "writeUId": UserService.get_mock(),
            "writeAt": now,
            "createUId": UserService.get_mock(),
            "createAt": now,
            "endAt": now,
        }

    def is_valid(cls, my_audit: dict) -> list:
        errors = list()

        if my_audit.get("createUId") is None:
            errors.append("Create User is required")

        my_writeAt = my_audit.get("writeAt")
        if my_writeAt is not None:
            if not CustomDatetime.check_format(my_writeAt):
                errors.append(SCHEMA_NOT_MATCH)

        my_createAt = my_audit.get("createAt")
        if my_createAt is not None:
            if not CustomDatetime.check_format(my_createAt):
                errors.append(SCHEMA_NOT_MATCH)

        my_createAt = my_audit.get("endAt")
        if my_createAt is not None:
            if not CustomDatetime.check_format(my_createAt):
                errors.append(SCHEMA_NOT_MATCH)

        return errors

    @classmethod
    def get_identifier(cls, user_id) -> IdentifierHandler | HandlerError:
        if not UserService.is_valid_user_id(user_id):
            raise HandlerError(ID_NOT_FOUND)
        return IdentifierHandler(IdentifierAlgorithm.DEFAULT, user_id)

    @classmethod
    def from_dict(cls, params: dict) -> dict | HandlerError:
        if params.get("writeUId") is None:
            raise HandlerError(WRITER_NOT_FOUND)

        if not UserService.is_valid_user_id(params.get("writeUId")):
            raise HandlerError(ID_NOT_FOUND)

        audit_dto = dict()
        for k in cls._fields:
            audit_dto[k] = params[k] if params.get(k) is not None else None

        errors = cls.is_valid(params)
        if len(errors) > 0:
            raise HandlerError("\n".join(errors))

        return audit_dto

    @classmethod
    def get_update_fields(cls, current_uid) -> dict | HandlerError:
        if not UserService.is_valid_user_id(current_uid):
            raise HandlerError(ID_NOT_FOUND)
        return {"writeUId": current_uid, "writeAt": CustomDatetime.str_now()}

    @classmethod
    def get_create_fields(cls, current_uid) -> dict | HandlerError:
        if not UserService.is_valid_user_id(current_uid):
            raise HandlerError(ID_NOT_FOUND)

        now = CustomDatetime.str_now()
        return {
            "writeUId": current_uid,
            "writeAt": now,
            "createUId": current_uid,
            "createAt": now,
            "endAt": None,
        }

    @classmethod
    def get_end_fields(cls, current_uid) -> dict | HandlerError:
        if not UserService.is_valid_user_id(current_uid):
            raise HandlerError(ID_NOT_FOUND)

        now = CustomDatetime.str_now()
        return {
            "writeUId": current_uid,
            "writeAt": now,
            "endAt": now,
        }
