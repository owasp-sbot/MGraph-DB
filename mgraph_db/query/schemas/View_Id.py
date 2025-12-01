from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id


class View_Id(Obj_Id):                         # helper class so that we don't use View_Id to represent the view_id class
    def __new__(cls, value=None):
        if value is None or value == '':
            return str.__new__(cls, '')
        else:
            return super().__new__(cls, value)