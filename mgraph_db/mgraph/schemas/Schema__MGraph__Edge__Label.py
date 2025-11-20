from osbot_utils.type_safe.Type_Safe                              import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id import Safe_Id


class Schema__MGraph__Edge__Label(Type_Safe):
    incoming    : Safe_Id = None
    outgoing    : Safe_Id = None
    predicate   : Safe_Id = None
