from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph                             import Schema__MGraph__Graph
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Graph__Config import Schema__File_System__Graph__Config


class Schema__File_System__Graph(Schema__MGraph__Graph):
    graph_config: Schema__File_System__Graph__Config