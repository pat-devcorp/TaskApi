from ..utils.ResponseHandler import ResponseDTO


class DomainError(Exception):
    def __init__(self, ref_response: ResponseDTO, message=""):
        self.message = message
        self.response = ref_response

    def __str__(self):
        return str(self.message)
