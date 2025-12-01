from typing                                                         import Set, Dict, Any, Optional
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from mgraph_db.query.models.Model__MGraph__Query__View              import Model__MGraph__Query__View
from mgraph_db.query.schemas.Schema__MGraph__Query__View            import Schema__MGraph__Query__View
from mgraph_db.query.schemas.Schema__MGraph__Query__View__Data      import Schema__MGraph__Query__View__Data
from mgraph_db.query.schemas.Schema__MGraph__Query__Views           import Schema__MGraph__Query__Views
from mgraph_db.query.schemas.View_Id import View_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id


class Model__MGraph__Query__Views(Type_Safe):
    data: Schema__MGraph__Query__Views

    def add_view(self, nodes_ids     : Set[Node_Id]             ,
                       edges_ids     : Set[Edge_Id]             ,
                       operation     : str                      ,       # refactor to Type_Safe primitive
                       params        : Dict[str, Any]           ,       # refactor to Type_Safe primitive
                       previous_id   : Optional[View_Id] = None
                 )                  -> Model__MGraph__Query__View:

        view_id = View_Id(Obj_Id())
        view    = Schema__MGraph__Query__View( view_id   = view_id,
                                               view_data = Schema__MGraph__Query__View__Data(nodes_ids        = nodes_ids   ,
                                                                                             edges_ids        = edges_ids   ,
                                                                                             query_operation  = operation   ,
                                                                                             query_params     = params      ,
                                                                                             previous_view_id = previous_id ))

        if previous_id and previous_id in self.data.views:
            self.data.views[previous_id].view_data.next_view_ids.add(view_id)

        self.data.views[view_id] = view

        if not self.data.first_view_id:
            self.data.first_view_id = view_id
        self.data.current_view_id = view_id

        return Model__MGraph__Query__View(data=view)

    def get_view(self, view_id: View_Id) -> Optional[Model__MGraph__Query__View]:
        if view_id in self.data.views:
            return Model__MGraph__Query__View(data=self.data.views[view_id])
        return None

    def current_view(self) -> Optional[Model__MGraph__Query__View]:
        if self.data.current_view_id:
            return self.get_view(self.data.current_view_id)
        return None

    def first_view(self) -> Optional[Model__MGraph__Query__View]:
        if self.data.first_view_id:
            return self.get_view(self.data.first_view_id)
        return None

    def set_current_view(self, view_id: View_Id) -> bool:
        if view_id in self.data.views:
            self.data.current_view_id = view_id
            return True
        return False

    def remove_view(self, view_id: View_Id) -> bool:
        if view_id not in self.data.views:
            return False

        view = self.data.views[view_id]

        # Update previous view's next_view_ids
        if view.view_data.previous_view_id:
            prev_view = self.data.views[view.view_data.previous_view_id]
            prev_view.view_data.next_view_ids.remove(view_id)

        # Update next views' previous_view_id
        for next_id in view.view_data.next_view_ids:
            if next_id in self.data.views:
                self.data.views[next_id].view_data.previous_view_id = view.view_data.previous_view_id

        # Remove the view
        del self.data.views[view_id]

        # Update first_view_id if needed
        if self.data.first_view_id == view_id:
            self.data.first_view_id = next(iter(view.view_data.next_view_ids)) if view.view_data.next_view_ids else None

        # Update current_view_id if needed
        if self.data.current_view_id == view_id:
            self.data.current_view_id = view.view_data.previous_view_id

        return True


