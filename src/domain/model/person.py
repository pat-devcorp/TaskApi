from collections import namedtuple

from ...infrastructure.bootstrap import constant
from ...utils.custom_date import CustomDate
from .status_code import FIELD_REQUIRED, ID_NOT_FOUND, INVALID_FORMAT
from ..custom_dict import CustomDict
from ..custom_string import CustomString
from ..DomainError import DomainError
from ..enum.contact_type import ContactType
from ..enum.identifier_algorithm import IdentifierAlgorithm
from ..identifier_handler import IdentifierHandler

Person = namedtuple(
    "Person",
    [
        "person_id",
        "name",
        "last_name",
        "contact_type",
        "birthdate",
        "document_number",
        "attrs",
    ],
)


class PersonDomain:
    algorithm = IdentifierAlgorithm.NANO_ID
    pk = "person_id"

    @staticmethod
    def get_invalid_person():
        return Person(
            person_id=0,
            name="Patrick Al0ns0",
            last_name="Fuent3s Carp1o",
            contact_type="A",
            birthdate="1995/07/18",
            document_number="@253",
            attrs=list(),
        )

    @classmethod
    def get_valid_person(cls):
        identifier = cls.get_default_identifier()
        return Person(
            person_id=identifier.value,
            name="Patrick Alonso",
            last_name="Fuentes Carpio",
            contact_type=ContactType.UNDEFINED.value,
            birthdate=CustomDate.not_available(),
            document_number=constant.NOT_AVAILABLE,
            attrs={
                "mail_address": "patrick18483@gmail.com",
                "address": "Cultura chimu 413",
                "zip_code": "04002",
            },
        )

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
    def from_dict(cls, data: list) -> Person | DomainError:
        if data.get(cls.pk) is None:
            raise DomainError(ID_NOT_FOUND, "id must be provided")

        item = {k: data.get(k, None) for k in Person._fields}
        attrs = {k: v for k, v in data.items() if k not in Person._fields}
        item["attrs"] = attrs

        cls.is_valid(**item)
        return Person(**item)

    @classmethod
    def is_valid(
        cls,
        person_id,
        name,
        last_name,
        contact_type,
        birthdate,
        document_number,
        attrs,
    ) -> Person | DomainError:
        errors = list()

        if person_id is None:
            errors.append("Id must be provided")
        else:
            try:
                cls.set_identifier(person_id)
            except DomainError as e:
                errors.append(str(e))

        if name is not None:
            if any(character.isdigit() for character in name):
                errors.append("name contain numbers")

        if last_name is not None:
            if any(character.isdigit() for character in last_name):
                errors.append("last_name contain numbers")

        if contact_type is not None:
            if not ContactType.has_value(contact_type):
                errors.append("Invalid contact type")

        if birthdate is not None and not (birthdate == CustomDate.not_available()):
            is_ok, err = CustomDate.check_format(birthdate)
            if not is_ok:
                errors.append(err)

        if (
            document_number is not None
            and not isinstance(document_number, str)
            and not (document_number == constant.NOT_AVAILABLE)
        ):
            if not document_number.isalnum():
                errors.append("Invalid document number")

        if attrs is not None:
            if not CustomDict.has_only_primitive_types(attrs):
                errors.append("the dictionary must have only primitive types")

        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))

    @classmethod
    def new(
        cls,
        person_id: IdentifierHandler,
        name: str,
        last_name: str,
        contact_type: ContactType | int,
        birthdate: str = None,
        document_number: str = None,
        attrs: dict = None,
    ) -> Person | DomainError:
        if (
            not isinstance(person_id, IdentifierHandler)
            or CustomString.is_empty_string(name)
            or CustomString.is_empty_string(last_name)
            or not isinstance(contact_type, (ContactType, int))
        ):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")
        contact_value = (
            contact_type.value
            if isinstance(contact_type, ContactType)
            else contact_type
        )
        if birthdate is None:
            birthdate = CustomDate.not_available()
        if document_number is None:
            document_number = constant.NOT_AVAILABLE
        if attrs is None:
            attrs = dict()

        cls.is_valid(
            person_id.value,
            name,
            last_name,
            contact_value,
            birthdate,
            document_number,
            attrs,
        )
        return Person(
            person_id.value,
            name,
            last_name,
            contact_value,
            birthdate,
            document_number,
            attrs,
        )
