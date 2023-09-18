from enum import Enum, auto


class AccessModifier(Enum):
    PUBLIC = '+'
    PRIVATE = '-'
    PROTECTED = '#'
    DEFAULT = '~'
