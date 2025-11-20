from mgraph_db.mgraph.models.Model__MGraph__Node                        import Model__MGraph__Node
from mgraph_db.providers.file_system.schemas.Schema__File_System__Item  import Schema__File_System__Item
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property    import set_as_property


class Model__File_System__Item(Model__MGraph__Node):                                                      # Base model for filesystem items
    data: Schema__File_System__Item

    folder_name = set_as_property('data', 'folder_name')                                                 # Folder name property
    created_at  = set_as_property('data', 'created_at' )                                                 # Creation timestamp property
    modified_at = set_as_property('data', 'modified_at')                                                 # Modification timestamp property


