from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Edges  import Schema__MGraph__Index__Data__Edges
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Labels import Schema__MGraph__Index__Data__Labels
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Paths  import Schema__MGraph__Index__Data__Paths
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Types  import Schema__MGraph__Index__Data__Types
from osbot_utils.type_safe.Type_Safe__On_Demand                         import Type_Safe__On_Demand


class Schema__MGraph__Index__Data(Type_Safe__On_Demand):
    edges : Schema__MGraph__Index__Data__Edges   = None                                            # Edge-node structural data
    labels: Schema__MGraph__Index__Data__Labels  = None                                            # Label/predicate data
    paths : Schema__MGraph__Index__Data__Paths   = None                                            # Path data
    types : Schema__MGraph__Index__Data__Types   = None                                            # Type data