from collections import namedtuple

from ...utils.status_code import FIELD_REQUIRED, ID_NOT_FOUND, INVALID_FORMAT
from ..custom_dict import CustomDict
from ..custom_string import CustomString
from ..DomainError import DomainError
from ..enum.identifier_algorithm import IdentifierAlgorithm
from ..identifier_handler import IdentifierHandler

Document = namedtuple(
    "Document",
    [
        "document_id",
        "body",
        "attrs",
    ],
)


class DocumentDomain:
    algorithm = IdentifierAlgorithm.NANO_ID
    pk = "document_id"

    @classmethod
    def get_default_identifier(cls) -> IdentifierHandler:
        return IdentifierHandler.get_default_identifier(cls.algorithm)

    @classmethod
    def set_identifier(cls, identifier) -> IdentifierHandler:
        return IdentifierHandler.is_valid(cls.algorithm, identifier)

    @staticmethod
    def as_dict(namedtuple_instance) -> dict:
        return dict(namedtuple_instance._asdict())

    @classmethod
    def from_dict(cls, data: list) -> Document | DomainError:
        if data.get(cls.pk) is None:
            raise DomainError(ID_NOT_FOUND, "id must be provided")

        item = {k: data.get(k, None) for k in Document._fields}
        attrs = {k: v for k, v in data.items() if k not in Document._fields}
        item["attrs"] = attrs

        cls.is_valid(**item)
        return Document(**item)

    @classmethod
    def is_valid(
        cls,
        document_id,
        body,
        attrs,
    ) -> Document | DomainError:
        errors = list()

        if document_id is None:
            errors.append("Id must be provided")
        else:
            try:
                cls.set_identifier(document_id)
            except DomainError as e:
                errors.append(str(e))

        if attrs is not None:
            if not CustomDict.has_only_primitive_types(attrs):
                errors.append("the dictionary must have only primitive types")

        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))

    @classmethod
    def new(
        cls,
        document_id: IdentifierHandler,
        body: str,
        attrs: dict = None,
    ) -> Document | DomainError:
        if not isinstance(
            document_id, IdentifierHandler
        ) or CustomString.is_empty_string(body):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")
        if attrs is None:
            attrs = dict()

        cls.is_valid(
            document_id.value,
            body,
            attrs,
        )
        return Document(
            document_id.value,
            CustomString.sanitize_string(body),
            attrs,
        )
