from ..custom_enum import CustomEnum


class CommitType(CustomEnum):
    UNDEFINED = 0
    FEAT = 1
    FIX = 2
    BUILD = 3
    CI = 4
    DOCS = 5
    CHORE = 6
    PERFORMANCE = 7
    REFACTOR = 8
    STYLE = 9
    TEST = 10
