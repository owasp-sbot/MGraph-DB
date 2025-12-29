from typing                                                               import Set, Dict, Optional
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                        import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Labels   import Schema__MGraph__Index__Data__Labels
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id         import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id         import Safe_Id
from osbot_utils.type_safe.Type_Safe                                      import Type_Safe


class MGraph__Index__Labels(Type_Safe):
    data    : Schema__MGraph__Index__Data__Labels  = None                                   # Dedicated labels index data
    enabled : bool = True                                                                   # Whether label indexing is active


    # =========================================================================
    # Add Methods
    # =========================================================================

    def add_edge_label(self, edge: Schema__MGraph__Edge) -> None:                            # Index edge labels (predicate, incoming, outgoing)
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        if edge.edge_label:
            edge_id = edge.edge_id

            if edge.edge_label.predicate:                                                    # Index by predicate
                predicate = edge.edge_label.predicate
                self.data.edges_predicates[edge_id] = predicate                              # Store edge_id to predicate mapping

                if predicate not in self.data.edges_by_predicate:                            # Store predicate to edge_id mapping
                    self.data.edges_by_predicate[predicate] = set()
                self.data.edges_by_predicate[predicate].add(edge_id)

            if edge.edge_label.incoming:                                                     # Index by incoming label
                incoming = edge.edge_label.incoming
                self.data.edges_incoming_labels[edge_id] = incoming                          # Store reverse mapping
                if incoming not in self.data.edges_by_incoming_label:
                    self.data.edges_by_incoming_label[incoming] = set()
                self.data.edges_by_incoming_label[incoming].add(edge_id)

            if edge.edge_label.outgoing:                                                     # Index by outgoing label
                outgoing = edge.edge_label.outgoing
                self.data.edges_outgoing_labels[edge_id] = outgoing                          # Store reverse mapping
                if outgoing not in self.data.edges_by_outgoing_label:
                    self.data.edges_by_outgoing_label[outgoing] = set()
                self.data.edges_by_outgoing_label[outgoing].add(edge_id)

    # =========================================================================
    # Remove Methods
    # =========================================================================

    def remove_edge_label(self, edge: Schema__MGraph__Edge) -> None:                         # Remove edge labels from index
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        edge_id = edge.edge_id

        if edge.edge_label and edge.edge_label.predicate:                                    # Remove from predicate indexes
            predicate = edge.edge_label.predicate
            if predicate in self.data.edges_by_predicate:
                self.data.edges_by_predicate[predicate].discard(edge_id)
                if not self.data.edges_by_predicate[predicate]:
                    del self.data.edges_by_predicate[predicate]

            if edge_id in self.data.edges_predicates:
                del self.data.edges_predicates[edge_id]

        if edge.edge_label and edge.edge_label.incoming:                                     # Remove from incoming label index
            incoming = edge.edge_label.incoming
            if incoming in self.data.edges_by_incoming_label:
                self.data.edges_by_incoming_label[incoming].discard(edge_id)
                if not self.data.edges_by_incoming_label[incoming]:
                    del self.data.edges_by_incoming_label[incoming]

        if edge.edge_label and edge.edge_label.outgoing:                                     # Remove from outgoing label index
            outgoing = edge.edge_label.outgoing
            if outgoing in self.data.edges_by_outgoing_label:
                self.data.edges_by_outgoing_label[outgoing].discard(edge_id)
                if not self.data.edges_by_outgoing_label[outgoing]:
                    del self.data.edges_by_outgoing_label[outgoing]

    def remove_edge_label_by_id(self, edge_id: Edge_Id) -> None:                             # Remove edge labels using only edge ID
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        predicate = self.data.edges_predicates.pop(edge_id, None)                            # Remove from predicate indexes
        if predicate and predicate in self.data.edges_by_predicate:
            self.data.edges_by_predicate[predicate].discard(edge_id)
            if not self.data.edges_by_predicate[predicate]:
                del self.data.edges_by_predicate[predicate]

        incoming = self.data.edges_incoming_labels.pop(edge_id, None)                        # Remove from incoming label index
        if incoming and incoming in self.data.edges_by_incoming_label:
            self.data.edges_by_incoming_label[incoming].discard(edge_id)
            if not self.data.edges_by_incoming_label[incoming]:
                del self.data.edges_by_incoming_label[incoming]

        outgoing = self.data.edges_outgoing_labels.pop(edge_id, None)                        # Remove from outgoing label index
        if outgoing and outgoing in self.data.edges_by_outgoing_label:
            self.data.edges_by_outgoing_label[outgoing].discard(edge_id)
            if not self.data.edges_by_outgoing_label[outgoing]:
                del self.data.edges_by_outgoing_label[outgoing]

    # =========================================================================
    # Query Methods
    # =========================================================================

    def get_edge_predicate(self, edge_id: Edge_Id) -> Optional[Safe_Id]:                     # Get predicate for a specific edge
        return self.data.edges_predicates.get(edge_id)

    def get_edges_by_predicate(self, predicate: Safe_Id) -> Set[Edge_Id]:                    # Get edges by predicate
        return self.data.edges_by_predicate.get(predicate, set())

    def get_edges_by_incoming_label(self, label: Safe_Id) -> Set[Edge_Id]:                   # Get edges by incoming label
        return self.data.edges_by_incoming_label.get(label, set())

    def get_edges_by_outgoing_label(self, label: Safe_Id) -> Set[Edge_Id]:                   # Get edges by outgoing label
        return self.data.edges_by_outgoing_label.get(label, set())

    def get_all_predicates(self) -> Set[Safe_Id]:                                            # Get all unique predicates
        return set(self.data.edges_by_predicate.keys())

    def get_all_incoming_labels(self) -> Set[Safe_Id]:                                       # Get all unique incoming labels
        return set(self.data.edges_by_incoming_label.keys())

    def get_all_outgoing_labels(self) -> Set[Safe_Id]:                                       # Get all unique outgoing labels
        return set(self.data.edges_by_outgoing_label.keys())

    def has_predicate(self, predicate: Safe_Id) -> bool:                                     # Check if predicate exists
        return predicate in self.data.edges_by_predicate

    def has_incoming_label(self, label: Safe_Id) -> bool:                                    # Check if incoming label exists
        return label in self.data.edges_by_incoming_label

    def has_outgoing_label(self, label: Safe_Id) -> bool:                                    # Check if outgoing label exists
        return label in self.data.edges_by_outgoing_label

    def count_edges_by_predicate(self, predicate: Safe_Id) -> int:                           # Count edges with predicate
        return len(self.data.edges_by_predicate.get(predicate, set()))

    def count_edges_by_incoming_label(self, label: Safe_Id) -> int:                          # Count edges with incoming label
        return len(self.data.edges_by_incoming_label.get(label, set()))

    def count_edges_by_outgoing_label(self, label: Safe_Id) -> int:                          # Count edges with outgoing label
        return len(self.data.edges_by_outgoing_label.get(label, set()))

    # =========================================================================
    # Raw Data Accessors
    # =========================================================================

    def edges_predicates(self) -> Dict[Edge_Id, Safe_Id]:                                    # Raw accessor for edges_predicates
        return self.data.edges_predicates

    def edges_by_predicate(self) -> Dict[Safe_Id, Set[Edge_Id]]:                             # Raw accessor for edges_by_predicate
        return self.data.edges_by_predicate

    def edges_incoming_labels(self) -> Dict[Edge_Id, Safe_Id]:                               # Raw accessor for edges_incoming_labels
        return self.data.edges_incoming_labels

    def edges_by_incoming_label(self) -> Dict[Safe_Id, Set[Edge_Id]]:                        # Raw accessor for edges_by_incoming_label
        return self.data.edges_by_incoming_label

    def edges_outgoing_labels(self) -> Dict[Edge_Id, Safe_Id]:                               # Raw accessor for edges_outgoing_labels
        return self.data.edges_outgoing_labels

    def edges_by_outgoing_label(self) -> Dict[Safe_Id, Set[Edge_Id]]:                        # Raw accessor for edges_by_outgoing_label
        return self.data.edges_by_outgoing_label