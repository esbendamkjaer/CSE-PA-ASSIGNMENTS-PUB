from enum import Enum


class ClassRelationship(Enum):
    COMPOSITION = 'composition'
    REALIZATION = 'realization'
    AGGREGATION = 'aggregation'
    INHERITANCE = 'inheritance'
    USES = 'uses'
