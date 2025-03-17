from mgraph_db.providers.graph_rag.mgraph.MGraph__Graph_RAG__Entity     import MGraph__Graph_RAG__Entity
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity    import Schema__Graph_RAG__Entity
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Nodes     import Schema__MGraph__RAG__Node__Source_Id, Schema__MGraph__RAG__Node__Text_Id, Schema__MGraph__RAG__Node__Entity, Schema__MGraph__RAG__Node__Concept, Schema__MGraph__RAG__Node__Role, Schema__MGraph__RAG__Node__Domain, Schema__MGraph__RAG__Node__Standard, Schema__MGraph__RAG__Node__Platform, Schema__MGraph__RAG__Node__Technology
from osbot_utils.decorators.methods.cache_on_self                       import cache_on_self
from osbot_utils.helpers.Obj_Id                                         import Obj_Id
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                         import type_safe

class Graph_RAG__Create_MGraph(Type_Safe):
    mgraph_entity          : MGraph__Graph_RAG__Entity
    config__add_group_nodes: bool           = False
    dot_code               : str            = None
    png_bytes              : bytes          = None
    png_save_to            : str            = None

    def setup(self):
        with self.builder() as _:
            _.config__unique_values = False
        return self

    def add_entities(self, entities):
        for entity in entities:
            self.add_entity(entity)
        return self

    def add__text_id(self, source_id: Obj_Id):
        return self.builder().add_node(value=source_id, node_type=Schema__MGraph__RAG__Node__Text_Id)

    def add__source_id(self, source_id: Obj_Id):
        return self.builder().add_node(value=source_id, node_type=Schema__MGraph__RAG__Node__Source_Id)

    def link__text_id(self, text_id: Obj_Id):
        return self.builder().add_predicate("text-id", text_id, node_type=Schema__MGraph__RAG__Node__Text_Id)

    def link__concept   (self, target: str, link_type="concept" ):   return self.builder().add_predicate(link_type, target, node_type=Schema__MGraph__RAG__Node__Concept   )
    def link__entity    (self, target: str, link_type="entity"  ):   return self.builder().add_predicate(link_type, target, node_type=Schema__MGraph__RAG__Node__Entity    )
    def link__role      (self, target: str, link_type="role"    ):   return self.builder().add_predicate(link_type, target, node_type=Schema__MGraph__RAG__Node__Role      )
    def link__domain    (self, target: str, link_type="domain"  ):   return self.builder().add_predicate(link_type, target, node_type=Schema__MGraph__RAG__Node__Domain    )
    def link__standard  (self, target: str, link_type="domain"  ):   return self.builder().add_predicate(link_type, target, node_type=Schema__MGraph__RAG__Node__Standard  )
    def link__platform  (self, target: str, link_type="platform"):   return self.builder().add_predicate(link_type, target, node_type=Schema__MGraph__RAG__Node__Platform  )
    def link__technology(self, target: str, link_type="platform"):   return self.builder().add_predicate(link_type, target, node_type=Schema__MGraph__RAG__Node__Technology)

    def add__direct_relationships(self, entity: Schema__Graph_RAG__Entity):
        with self.builder() as _:
            if self.config__add_group_nodes:
                _.add_predicate('direct', 'relationships', key=Obj_Id())
            for direct_relationship in entity.direct_relationships:
                target    = direct_relationship.entity
                link_type = direct_relationship.relationship_type
                self.link__entity(target=target, link_type=link_type).up()
            if self.config__add_group_nodes:
                _.up()

    def add__domain_relationships(self, entity: Schema__Graph_RAG__Entity):
        with self.builder() as _:
            if self.config__add_group_nodes:
                _.add_predicate('domain', 'relationships', key=Obj_Id())
            for domain_relationship in entity.domain_relationships:
                target    = domain_relationship.concept
                link_type = domain_relationship.relationship_type
                self.link__concept(target=target, link_type=link_type).up()
            if self.config__add_group_nodes:
                _.up()

    def add__roles(self, entity: Schema__Graph_RAG__Entity):
        with self.builder() as _:
            if self.config__add_group_nodes:
                _.add_predicate('has', 'functional_roles', key=Obj_Id())
            for role in entity.functional_roles:
                self.link__role(target=role).up()
            if self.config__add_group_nodes:
                _.up()

    def add__primary_domains(self, entity: Schema__Graph_RAG__Entity):
        with self.builder() as _:
            if self.config__add_group_nodes:
                _.add_predicate('has', 'primary_domains', key=Obj_Id())
            for domain in entity.primary_domains:
                self.link__domain(target=domain).up()
            if self.config__add_group_nodes:
                _.up()

    def add__platforms(self, entity: Schema__Graph_RAG__Entity):
        if entity.ecosystem.platforms:
            with self.builder() as _:
                if self.config__add_group_nodes:
                    _.add_predicate('uses', 'platforms', key=Obj_Id())
                for platform in entity.ecosystem.platforms:
                    self.link__platform(target=platform).up()
                if self.config__add_group_nodes:
                    _.up()

    def add__technologies(self, entity: Schema__Graph_RAG__Entity):
        if entity.ecosystem.technologies:
            with self.builder() as _:
                if self.config__add_group_nodes:
                    _.add_predicate('uses', 'technologies', key=Obj_Id())
                for technology in entity.ecosystem.technologies:
                    self.link__technology(target=technology).up()
                if self.config__add_group_nodes:
                    _.up()

    def add__standards(self, entity: Schema__Graph_RAG__Entity):
        if entity.ecosystem.standards:
            with self.builder() as _:
                if self.config__add_group_nodes:
                    _.add_predicate('uses', 'standards', key=Obj_Id())
                for standard in entity.ecosystem.standards:
                    self.link__standard(target=standard).up()
                if self.config__add_group_nodes:
                    _.up()

    def add__source_and_text_ids(self, entity: Schema__Graph_RAG__Entity):
        with self.builder() as _:
            if entity.source_id:
                self.add__source_id(entity.source_id)
                self.link__text_id (entity.text_id  )
            else:
                self.add__text_id(entity.text_id)
    @type_safe
    def add_entity(self, entity: Schema__Graph_RAG__Entity):
        with self.builder() as _:
            _.root()
            self.add__source_and_text_ids (entity)
            #_.new_node()
            self.link__entity             (entity.name)
            self.add__direct_relationships(entity)                          # adding direct relationships (as entities)
            self.add__domain_relationships(entity)                          # adding domain relationships (as concepts)
            self.add__roles               (entity)
            self.add__primary_domains     (entity)
            self.add__platforms           (entity)                               # adding ecosystem
            self.add__standards           (entity)
            self.add__technologies        (entity)
            _.up()
        return self

    @cache_on_self
    def builder(self):
        return self.mgraph_entity.builder()

    @cache_on_self
    def screenshot(self):
        return self.mgraph_entity.screenshot()

    def screenshot__add_colors(self):
        with self.screenshot() as _:
            with _.export().export_dot() as dot:
                color__source_id  = '#B0E0E6'  # Powder Blue - for source nodes
                color__text_id    = '#D3D3D3'  # Light Gray - for text ID nodes
                color__entity     = '#7EB36A'  # Sage Green - for entity nodes
                color__value      = '#F5F5F5'  # White Smoke - for value nodes
                color__concept    = '#6495ED'  # Cornflower Blue - for concept nodes
                color__domain     = '#87CEFA'  # Light Sky Blue - for domain nodes
                color__role       = '#98C1D9'  # Blue Gray - for role nodes
                color__standard   = '#7CB9E8'  # Carolina Blue - for standard nodes
                color__platform   = '#FFB9E8'
                color__technology = '#AAC1D9'


                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Source_Id , color__source_id )
                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Text_Id   , color__text_id   )
                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Entity    , color__entity    )
                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Concept   , color__concept   )
                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Domain    , color__domain    )
                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Role      , color__role      )
                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Standard  , color__standard  )
                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Platform  , color__platform  )
                dot.set_node__type_fill_color(Schema__MGraph__RAG__Node__Technology, color__technology)

    def screenshot__setup(self):
        with self.screenshot().export().export_dot() as _:
                # if self.use_layout_engine__sfdp:
                #     dot.set_graph__layout_engine__sfdp()
                #     #dot.set_graph__layout_engine__circo()
                #     dot.set_graph__spring_constant    (0.1)
                #     dot.set_graph__overlap__scale     ()
                # else:
                _.set_graph__rank_dir__lr()
                _.set_node__shape__type__box()
                _.set_node__shape__rounded()
                _.show_edge__predicate__str()
                #_.set_graph__splines__ortho()

                #dot.show_node__type      ()
                _.show_node__value     ()
                #dot.show_node__value__key()
                #dot.set_render__label_show_var_name()

    def screenshot__create_bytes(self):
        with self.screenshot() as _:
            dot_code       = self.screenshot__create_dot_code()
            self.png_bytes = _.dot_to_png(dot_code)
            return self.png_bytes

    def screenshot__create_file(self, target_file):
        self.screenshot().save_to(target_file)
        self.screenshot__create_bytes()

    def screenshot__create_dot_code(self):
        with self as _:
            _.screenshot__setup()
            _.screenshot__add_colors()
            self.dot_code = _.screenshot().export().to__dot()
            return self.dot_code