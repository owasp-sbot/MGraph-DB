from typing                          import List
from osbot_utils.type_safe.Type_Safe import Type_Safe


# todo:refactored str below to Type_Safe class
class PlantUML__Context(Type_Safe):                                                   # holds rendered statements
    nodes                : List[str]                                                  # rendered node statements
    edges                : List[str]                                                  # rendered edge statements
