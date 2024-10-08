import json
import traceback

from ..domain.DomainError import DomainError
from ..infrastructure.InfrastructureError import InfrastructureError
from ..presentation.PresentationError import PresentationError


def exception_handler(func):
    def wrapper(*args, **kwargs):
        response = ""
        status_code = 403

        try:
            status_code, response = func(*args, **kwargs) or "OK"
        except PresentationError as p_err:
            response = str(p_err)
            status_code = 422
        except DomainError as d_err:
            response = str(d_err)
            status_code = 500
        except InfrastructureError as i_err:
            response = str(i_err)
            status_code = 500
        except TimeoutError as t_err:
            response = str(t_err)
            status_code = 600
        except Exception as err:
            error = {
                "message": str(err),
                "traceback": traceback.format_exc(),
            }
            response = str(error)

        finally:
            return json.dumps({"data": response, "statusCode": status_code})

    # Renaming the function name:
    wrapper.__name__ = func.__name__

    return wrapper
