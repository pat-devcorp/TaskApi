from collections import namedtuple

ResponseDTO = namedtuple("ResponseDTO", ["error_id", "description"])

DEFAULT = ResponseDTO("1000", "CRASH_LOGIC")
ID_NOT_FOUND = ResponseDTO("1000", "ID must be provided")
ID_NOT_VALID = ResponseDTO("1000", "ID not valid")
WRITE_UID_NOT_FOUND = ResponseDTO("1000", "Writer must be provided")
FORMAT_NOT_MATCH = ResponseDTO("1000", "The format specificated is not valid")
UNSUPPORTED_MEDIA_TYPE = ResponseDTO("415", "This type of file is not supported")
WARNING_FILE = ResponseDTO("1000", "File could have pottential virus")
NOT_FOUND = ResponseDTO("404", "Not found")
OPERATION_FAIL = ResponseDTO("417", "Operation fail")
REQUIRED_FIELD = ResponseDTO("417", "Required param was not send")
IS_NOT_MEMBER = ResponseDTO("1000", "Required param was not send")
BROKER_CONNECTION_FAIL = ResponseDTO("1000", "Required param was not send")
BROKER_SEND_FAIL = ResponseDTO("1000", "Required param was not send")
DUPLICATE_ID = ResponseDTO("1000", "Id is present in repository")
DB_CONNECTION_ERROR = ResponseDTO("1000", "Databse server doesnt respond")
DB_COLLECTION_NOT_FOUND = ResponseDTO("1000", "Databse server doesnt respond")
DB_GET_FAIL = ResponseDTO("1000", "Databse server doesnt respond")
DB_CREATE_FAIL = ResponseDTO("1000", "Databse server doesnt respond")
DB_UPDATE_FAIL = ResponseDTO("1000", "Databse server doesnt respond")
DB_DELETE_FAIL = ResponseDTO("1000", "Databse server doesnt respond")
PRESENTATION_VALIDATION = ResponseDTO("1000", "Databse server doesnt respond")

# ERROR_REQUIRED_FIELD          = 1000
# ID_NOT_FOUND                  = 1001
# FAIL_CONVERTED_UUID_TO_STRING = 1002
# NO_CONTENT                    = 1003
# CRASH_LOGIC                   = 1004

# # CODE STATUS
# CODE_CONTINUE = 100
# CODE_SWITCHING_PROTOCOLS = 101
# CODE_PROCESSING = 102
# CODE_EARLYHINTS = 103
# CODE_OK = 200
# CODE_CREATED = 201
# CODE_ACCEPTED = 202
# CODE_NO_AUTHORITATIVE = 203
# CODE_NO_CONTENT = 204
# CODE_RESET_CONTENT = 205
# CODE_PARTIAL_CONTENT = 206
# CODE_MULTI_STATUS = 207
# CODE_ALREDY_REPORTED = 208
# CODE_IM_USED = 226
# CODE_MULTIPLE_CHOICES = 300
# CODE_MOVED_PERMANENTLY = 301
# CODE_FOUND = 302
# CODE_SEE_OTHER = 303
# CODE_NOT_MODIFIED = 304
# CODE_USE_PROXY = 305
# CODE_SWITCH_PROXY = 306
# CODE_TEMPORARY_REDIRECT = 307
# CODE_PERMANENT_REDIRECT = 308
# CODE_BAD_REQUEST = 400
# CODE_UNAUTHORIZED = 401
# CODE_PAYMENT_REQUIRED = 402
# CODE_FORBIDDEN = 403
# CODE_NOT_FOUND = 404
# CODE_METHOD_NOT_ALLOWED = 405
# CODE_NOT_ACEPTABLE = 406
# CODE_PROXY_AUTHENTICATION_REQUIRED = 407
# CODE_REQUEST_TIMEOUT = 408
# CODE_CONFLICT = 409
# CODE_GONE = 410
# CODE_LENGTH_REQUIRED = 411
# CODE_PRECONDITION_FAILED = 412
# CODE_PAYLOAD_TOO_LARGE = 413
# CODE_URI_TOO_LONG = 414
# CODE_UNSUPPORTED_MEDIA_TYPE = 415
# CODE_RANGE_NOT_SATISFIABLE = 416
# CODE_EXPECTATION_FAILED = 417
# CODE_IAM_A_TEAPOT = 418
# CODE_MISDIRECTED_REQUEST = 421
# CODE_UNPROCESSABLE_ENTITY = 422
# CODE_LOCKED = 423
# CODE_FAILED_DEPENDENCY = 424
# CODE_TOO_EARLY = 425
# CODE_UPGRADE_REQUIERED = 426
# CODE_PRECONDITION_REQUIRED = 428
# CODE_TOO_MANY_REQUESTS = 429
# CODE_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
# CODE_UNAVAILABLE_FOR_LEGAL_REASONS = 451
# CODE_INTERNAL_SERVER_ERROR = 500
# CODE_NOT_IMPLEMENTED = 501
# CODE_BAD_GATEWAY = 502
# CODE_SERVICE_UNAVAILABLE = 503
# CODE_GETWAY_TIMEOUT = 504
# CODE_HTTP_VERSION_NOT_SUPPORTED = 505
# CODE_VARIANT_ALSO_NEGOTIATES = 506
# CODE_INSUFFICIENT_STORAGE = 507
# CODE_LOOP_DETECTED = 508
# CODE_NOT_EXTENDED = 509
# CODE_NETWORK_AUTHENTICATION_REQUIRED = 511

# # RFC
# VALIDATE_PROVIDER_CALL="ZRFC_ER_VALIDAR_PROVEEDOR"