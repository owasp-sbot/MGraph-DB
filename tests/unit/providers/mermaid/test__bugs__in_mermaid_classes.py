from unittest                                                       import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                 import Schema__MGraph__Types
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node       import Domain__Mermaid__Node
from mgraph_db.providers.mermaid.models.Model__Mermaid__Graph       import Model__Mermaid__Graph
from mgraph_db.providers.mermaid.models.Model__Mermaid__Node        import Model__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Types     import Schema__Mermaid__Types
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph     import Schema__Mermaid__Graph


class test__bug__in_mermaid_classes(TestCase):

    def test__bug__json_roundtrip(self):
        # these will fail if
        #   attribute_type   : Type[Schema__MGraph__Attribute]
        # is not in Schema__Mermaid__Types
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'attribute_type'. Expected 'typing.Type[mgraph_db.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute]' but got '<class 'str'>'")):
        #     Mermaid__Node.from_json(Mermaid__Node().json())
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'attribute_type'. Expected 'typing.Type[mgraph_db.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute]' but got '<class 'str'>'")):
        #     Model__Mermaid__Graph.from_json(Model__Mermaid__Graph().json())
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'attribute_type'. Expected 'typing.Type[mgraph_db.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute]' but got '<class 'str'>'")):
        #     Schema__Mermaid__Graph.from_json(Schema__Mermaid__Graph().json())
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'attribute_type'. Expected 'typing.Type[mgraph_db.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute]' but got '<class 'str'>'")):
        #     Schema__Mermaid__Types.from_json(Schema__Mermaid__Types().json())

        # these only work with the attribute in there
        mermaid_node = Domain__Mermaid__Node()
        assert Domain__Mermaid__Node.from_json(mermaid_node.json()).json() == mermaid_node.json()
        Domain__Mermaid__Node                  .from_json(Domain__Mermaid__Node                  ().json())
        Model__Mermaid__Graph          .from_json(Model__Mermaid__Graph          ().json())
        Schema__Mermaid__Graph         .from_json(Schema__Mermaid__Graph         ().json())
        Schema__Mermaid__Types.from_json(Schema__Mermaid__Types().json())

        # these work without the attribute in there
        Schema__MGraph__Types.from_json(Schema__MGraph__Types().json())
        Model__Mermaid__Node.from_json(Model__Mermaid__Node().json())
