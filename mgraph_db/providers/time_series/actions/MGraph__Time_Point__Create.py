from typing                                                                               import Type, Tuple
from mgraph_db.mgraph.actions.MGraph__Edit                                                import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Values                                              import MGraph__Values
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                         import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                                        import Schema__MGraph__Edge
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Create__Data     import Schema__MGraph__Time_Point__Create__Data
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Created__Objects import Schema__MGraph__Time_Point__Created__Objects
from osbot_utils.decorators.methods.cache_on_self                                         import cache_on_self
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                         import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                         import Node_Id
from osbot_utils.type_safe.Type_Safe                                                      import Type_Safe


class MGraph__Time_Point__Create(Type_Safe):
    mgraph_edit : MGraph__Edit

    def execute(self, create_data: Schema__MGraph__Time_Point__Create__Data) -> Schema__MGraph__Time_Point__Created__Objects:
        time_point = self.mgraph_edit.new_node(node_type=create_data.node_type__time_point)

        if create_data.datetime_str:                                             # Set the display value if available
            time_point.node_data.value = create_data.datetime_str

        value_nodes__by_type = {}                                                     # Initialize tracking dictionaries
        value_edges__by_type = {}

        time_components = [(create_data.year     , create_data.edge_type__year     ),                # Define time components to process
                           (create_data.month    , create_data.edge_type__month    ),
                           (create_data.day      , create_data.edge_type__day      ),
                           (create_data.hour     , create_data.edge_type__hour     ),
                           (create_data.minute   , create_data.edge_type__minute   ),
                           (create_data.second   , create_data.edge_type__second   ),
                           (create_data.source_id, create_data.edge_type__source_id),
                           (create_data.timestamp, create_data.edge_type__timestamp)]

        for value, edge_type in time_components:                                 # Process each time component
            if value is not None:
                node_id, edge_id           = self.add_value_component(value      = value                       ,
                                                                      edge_type  = edge_type                   ,
                                                                      from_node  = time_point                  )
                value_nodes__by_type[edge_type] = node_id
                value_edges__by_type[edge_type] = edge_id

        created_objects = Schema__MGraph__Time_Point__Created__Objects(time_point__node_id  = time_point.node_id  ,
                                                                       value_nodes__by_type = value_nodes__by_type,
                                                                       value_edges__by_type = value_edges__by_type )

        if create_data.timezone:                                                    # Handle timezone if present
            self.add_timezone_component(created_objects = created_objects        ,
                                        timezone        = create_data.timezone   ,
                                        utc_offset      = create_data.utc_offset ,
                                        create_data     = create_data            ,
                                        time_point      = time_point             )


        return created_objects

    def add_timezone_component(self, created_objects: Schema__MGraph__Time_Point__Created__Objects,
                                     timezone       : str                                         ,
                                     utc_offset     : int                                         ,
                                     create_data    : Schema__MGraph__Time_Point__Create__Data    ,
                                     time_point     : Domain__MGraph__Node
                                ): #-> Tuple[Obj_Id, Obj_Id]:

        # Get or create timezone node using values system
        timezone__node, timezone__edge = self.values().get_or_create_value(value     = timezone                 ,
                                                                           edge_type = create_data.edge_type__tz,
                                                                           from_node = time_point               )
        created_objects.timezone__node_id = timezone__node.node_id
        created_objects.timezone__edge_id = timezone__edge.edge_id
        if utc_offset is not None:                                                                                  # Get or create UTC offset node using values system

            utc_offset__node, utc_offset__edge = self.values().get_or_create_value(value     = utc_offset                       ,
                                                                                   edge_type = create_data.edge_type__utc_offset,
                                                                                   from_node = timezone__node                   )
            created_objects.utc_offset__node_id = utc_offset__node.node_id
            created_objects.utc_offset__edge_id = utc_offset__edge.edge_id




    def add_value_component(self, value     : int                        ,                    # Add a value component to time point
                                  edge_type : Type[Schema__MGraph__Edge] ,
                                  from_node : Domain__MGraph__Node
                           ) -> Tuple[Node_Id, Edge_Id]:                                       # Returns value_node_id, edge_id

        value_node = self.values().get_or_create(value)                                  # Get or create value node

        edge = self.mgraph_edit.new_edge(edge_type    = edge_type          ,                 # Create edge to value
                                         from_node_id = from_node.node_id  ,
                                         to_node_id   = value_node.node_id )

        return value_node.node_id, edge.edge_id                                              # Return both IDs

    @cache_on_self
    def values(self) -> MGraph__Values:                                             # Value node factory accessor
        return MGraph__Values(mgraph_edit=self.mgraph_edit)