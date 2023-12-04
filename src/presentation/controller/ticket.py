from ...application.BrokerProtocol import BrokerProtocol
from ...application.ticket import Ticket as TicketUseCase
from ...domain.RepositoryProtocol import RepositoryProtocol
from ...infraestructure.broker.kafka import Kafka
from ...infraestructure.repositories.ticket_mongo import Ticket as TicketRepository
from ...presentation.PresentationError import PresentationError
from ..dto.ticket import TicketDTO
from ..IdentifierHandler import IdentifierHandler


class Ticket:
    def __init__(
        self,
        ref_write_uid,
        ref_repository: None | RepositoryProtocol = None,
        ref_broker: None | BrokerProtocol = None,
    ):
        self._w = ref_write_uid
        _r = TicketRepository() if ref_repository is None else ref_repository
        _b = Kafka.setToDefault() if ref_broker is None else ref_broker
        self._uc = TicketUseCase(self._w, _r, _b)

    @staticmethod
    def getTemplate() -> str:
        return """
            **I:** Patrick Alonso Fuentes Carpio

            **AS:** A developer, I need a task module.

            **I WANT TO:** Create a new task, associate users with different roles to the task, add meetings, link related words to the task for searching, conduct surveys, and maintain a list of milestones related to the task.

            **BECAUSE**: I want to enhance traceability and provide accurate statistics.

            **MILESTONES:**
            - Create, edit, and delete tasks.
            - Add team members.
            - Send notifications to team members based on task-related events.
            - Create surveys.
            - Schedule meetings.
            - Associate keywords with the task for searching.
            - Generate a task document.

            **NOTES:** The module should be developed following clean architecture principles.
            """

    @classmethod
    def prepareCreate(
        cls, dto_id: IdentifierHandler, params: dict
    ) -> TicketDTO | PresentationError:
        data = cls.filterKeys(params)
        return TicketDTO(dto_id, **data)

    @classmethod
    def prepareUpdate(
        cls, dto_id: IdentifierHandler, params: dict
    ) -> TicketDTO | PresentationError:
        data = cls.filterKeys(params)
        return TicketDTO.fromDict(dto_id, data)

    @staticmethod
    def prepareIdentifier(identifier) -> IdentifierHandler | PresentationError:
        return TicketDTO.getIdentifier(identifier)

    def fetch(self) -> list:
        datos = self._uc.fetch()
        return [TicketDTO.filterKeys(item) for item in datos]

    def create(self, dto: TicketDTO) -> bool:
        return self._uc.create(
            dto.ticket_id, dto.description, dto.category, dto.type_commit, dto.state
        )

    def update(self, dto: TicketDTO) -> bool:
        return self._uc.update(
            dto.ticket_id, dto.description, dto.category, dto.type_commit, dto.state
        )

    def getByID(self, dto_id: IdentifierHandler) -> dict:
        data = self._uc.getByID(dto_id)
        return TicketDTO.filterKeys(data)

    def delete(self, dto_id: IdentifierHandler):
        return self._uc.delete(dto_id)

    # def addKeyword(self, ticket_id: IdentifierHandler, keyword_id: IdentifierHandler):
    #     return self._uc.addKeyword(ticket_id.value, keyword_id.value)

    # def removeKeyword(self, ticket_id: IdentifierHandler, keyword_id: IdentifierHandler):
    #     pass

    # def addMeeting(self, ticket_id: IdentifierHandler, meeting_id: IdentifierHandler):
    #     pass

    # def removeMeeting(self, ticket_id: IdentifierHandler, meeting_id: IdentifierHandler):
    #     pass

    # def addMilestone(self, ticket_id: IdentifierHandler, milestone_id: IdentifierHandler):
    #     pass

    # def removeMilestone(
    #     self, ticket_id: IdentifierHandler, milestone_id: IdentifierHandler
    # ):
    #     pass

    # def addAttachment(self, ticket_id: IdentifierHandler, file_name: FileHanlder):
    #     pass

    # def removeAttachment(self, ticket_id: IdentifierHandler, file_name: FileHanlder):
    #     pass

    # def addMember(self, ticket_id: IdentifierHandler, member_id: IdentifierHandler):
    #     pass

    # def removeMember(self, ticket_id: IdentifierHandler, member_id: IdentifierHandler):
    #     pass

    # def setAssignee(self, ticket_id: IdentifierHandler, member_id: IdentifierHandler):
    #     pass