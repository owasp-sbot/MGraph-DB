from typing                                                                     import Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                             import Schema__MGraph__Types
from mgraph_db.providers.file_system.schemas.Schema__File_System__Graph__Config import Schema__File_System__Graph__Config
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                        import Schema__MGraph__Node__Data
from mgraph_db.providers.file_system.schemas.Schema__Folder__Node               import Schema__Folder__Node


class Schema__File_System__Types(Schema__MGraph__Types):
    graph_data_type  : Type[Schema__File_System__Graph__Config]
    node_type        : Type[Schema__Folder__Node              ]
    node_data_type   : Type[Schema__MGraph__Node__Data        ]         # todo: remove , since this is not needed here (same value as Schema__MGraph__Types)
