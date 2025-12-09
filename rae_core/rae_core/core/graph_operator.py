"""
Knowledge Graph Update Operator - Iteration 5

Mathematical formulation:
  G_{t+1} = T(G_t, o_t, a_t)

Where:
  G_t = (V_t, E_t) - Graph at time t
  o_t = Observation (new memory, entity extraction result, etc.)
  a_t = Action (add_node, add_edge, merge_nodes, prune, etc.)
  T = Deterministic transformation function

Properties to maintain:
  - Consistency: No duplicate nodes with same entity
  - Connectivity: Graph should remain connected
  - Temporal decay: Edge weights decay over time
  - Convergence: Graph should stabilize over time

Usage:
    operator = GraphUpdateOperator()

    # Load current graph
    G_t = await load_graph(tenant_id, project_id)

    # Observation: new memory with entities
    observation = {
        "memory_id": "mem_123",
        "content": "John met Alice at the conference",
        "entities": ["John", "Alice", "conference"],
        "relations": [("John", "met", "Alice"), ...]
    }

    # Apply transformation
    G_next = operator.apply(
        graph=G_t,
        action_type=GraphActionType.ADD_EDGE,
        observation=observation
    )

    # Analyze convergence
    convergence = operator.analyze_convergence(graph_history)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import numpy as np
import structlog


logger = structlog.get_logger(__name__)


class GraphActionType(str, Enum):
    """Types of graph transformations"""

    ADD_NODE = "add_node"
    ADD_EDGE = "add_edge"
    UPDATE_EDGE_WEIGHT = "update_edge_weight"
    MERGE_NODES = "merge_nodes"
    PRUNE_NODE = "prune_node"
    PRUNE_EDGE = "prune_edge"
    EXTRACT_SUBGRAPH = "extract_subgraph"


@dataclass
class GraphNode:
    """
    Node in knowledge graph.

    Represents entities, concepts, events in RAE memory.

    Attributes:
        id: Unique node identifier
        label: Human-readable label
        node_type: Type of entity (person, concept, event, etc.)
        properties: Additional metadata
        created_at: Creation timestamp
        last_updated: Last update timestamp
        importance: Importance score [0-1]
        centrality: Graph centrality score [0-1]
    """

    id: str
    label: str
    node_type: str  # entity, concept, event, etc.
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    importance: float = 0.5  # 0-1
    centrality: float = 0.0  # 0-1 (computed from graph structure)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "label": self.label,
            "node_type": self.node_type,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "importance": self.importance,
            "centrality": self.centrality,
        }


@dataclass
class GraphEdge:
    """
    Edge in knowledge graph.

    Represents relationships between entities.

    Attributes:
        id: Unique edge identifier (format: source_relation_target)
        source_id: Source node ID
        target_id: Target node ID
        relation: Relationship type
        weight: Edge weight [0-1]
        confidence: Confidence score [0-1]
        created_at: Creation timestamp
        last_updated: Last update timestamp
        evidence_count: Number of observations supporting this edge
    """

    id: str
    source_id: str
    target_id: str
    relation: str
    weight: float = 0.7  # 0-1
    confidence: float = 0.8  # 0-1
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    evidence_count: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation": self.relation,
            "weight": self.weight,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "evidence_count": self.evidence_count,
        }


@dataclass
class KnowledgeGraph:
    """
    Complete knowledge graph state.

    Mathematical formulation: G = (V, E)
      V = set of nodes (vertices)
      E = set of edges

    Attributes:
        nodes: Dictionary of node_id -> GraphNode
        edges: Dictionary of edge_id -> GraphEdge
        tenant_id: Tenant identifier
        project_id: Project identifier
        created_at: Graph creation timestamp
        last_updated: Last update timestamp
    """

    nodes: Dict[str, GraphNode] = field(default_factory=dict)
    edges: Dict[str, GraphEdge] = field(default_factory=dict)
    tenant_id: str = ""
    project_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get node by ID"""
        return self.nodes.get(node_id)

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        """Get edge by ID"""
        return self.edges.get(edge_id)

    def adjacency_matrix(self) -> np.ndarray:
        """
        Get adjacency matrix for graph analysis.

        Returns:
            Adjacency matrix A where A[i,j] = weight of edge from node i to node j
        """
        if not self.nodes:
            return np.array([[]])

        node_ids = list(self.nodes.keys())
        n = len(node_ids)
        adj = np.zeros((n, n))

        node_idx = {node_id: i for i, node_id in enumerate(node_ids)}

        for edge in self.edges.values():
            i = node_idx.get(edge.source_id)
            j = node_idx.get(edge.target_id)

            if i is not None and j is not None:
                adj[i][j] = edge.weight

        return adj

    def copy(self) -> "KnowledgeGraph":
        """Deep copy of graph"""
        import copy

        return copy.deepcopy(self)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "edges": {edge_id: edge.to_dict() for edge_id, edge in self.edges.items()},
            "tenant_id": self.tenant_id,
            "project_id": self.project_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
        }


class GraphUpdateOperator:
    """
    Implements graph transformation function T.

    Mathematical formulation:
      G_{t+1} = T(G_t, o_t, a_t)

    Where:
      - G_t: Current graph state
      - o_t: Observation (new information)
      - a_t: Action (transformation to apply)
      - T: Deterministic transformation function

    This operator ensures:
      1. Deterministic transformations (reproducible)
      2. Temporal decay of edge weights
      3. Entity resolution (merge duplicates)
      4. Convergence to stable structure

    Usage:
        operator = GraphUpdateOperator(
            edge_half_life_days=30.0,
            edge_prune_threshold=0.1,
            merge_similarity_threshold=0.9
        )

        # Apply transformation
        G_next = operator.apply(
            graph=G_t,
            action_type=GraphActionType.ADD_EDGE,
            observation={"edge_data": {...}},
            parameters={}
        )

        # Analyze convergence
        convergence = operator.analyze_convergence(graph_history)
    """

    def __init__(
        self,
        edge_half_life_days: float = 30.0,
        edge_prune_threshold: float = 0.1,
        merge_similarity_threshold: float = 0.9,
    ):
        """
        Initialize graph operator.

        Args:
            edge_half_life_days: Half-life for edge weight decay (exponential decay)
            edge_prune_threshold: Below this weight, edges are pruned
            merge_similarity_threshold: Above this similarity, nodes are merged
        """
        self.edge_half_life_days = edge_half_life_days
        self.edge_prune_threshold = edge_prune_threshold
        self.merge_similarity_threshold = merge_similarity_threshold

        logger.info(
            "graph_operator_initialized",
            edge_half_life_days=edge_half_life_days,
            edge_prune_threshold=edge_prune_threshold,
            merge_similarity_threshold=merge_similarity_threshold,
        )

    def apply(
        self,
        graph: KnowledgeGraph,
        action_type: GraphActionType,
        observation: Dict[str, Any],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> KnowledgeGraph:
        """
        Apply graph transformation: G_{t+1} = T(G_t, o_t, a_t)

        This is the core transformation function T.

        Args:
            graph: Current graph state G_t
            action_type: Type of transformation (a_t)
            observation: Observation o_t (new data)
            parameters: Optional action parameters

        Returns:
            New graph state G_{t+1}
        """
        with tracer.start_as_current_span("rae.graph.transform") as span:
            # Validate action_type is a GraphActionType enum
            if not isinstance(action_type, GraphActionType):
                raise ValueError(
                    f"action_type must be GraphActionType enum, got {type(action_type)}"
                )

            parameters = parameters or {}

            span.set_attribute("rae.graph.action_type", action_type.value)
            span.set_attribute("rae.tenant_id", graph.tenant_id)
            span.set_attribute("rae.project_id", graph.project_id)
            span.set_attribute("rae.graph.nodes_before", len(graph.nodes))
            span.set_attribute("rae.graph.edges_before", len(graph.edges))

            logger.info(
                "graph_transformation_started",
                action_type=action_type.value,
                nodes_before=len(graph.nodes),
                edges_before=len(graph.edges),
            )

            # Copy graph (immutable transformation)
            G_next = graph.copy()

            # Apply transformation based on action type
            if action_type == GraphActionType.ADD_NODE:
                G_next = self._add_node(G_next, observation, parameters)

            elif action_type == GraphActionType.ADD_EDGE:
                G_next = self._add_edge(G_next, observation, parameters)

            elif action_type == GraphActionType.UPDATE_EDGE_WEIGHT:
                G_next = self._update_edge_weight(G_next, observation, parameters)

            elif action_type == GraphActionType.MERGE_NODES:
                G_next = self._merge_nodes(G_next, observation, parameters)

            elif action_type == GraphActionType.PRUNE_NODE:
                G_next = self._prune_node(G_next, observation, parameters)

            elif action_type == GraphActionType.PRUNE_EDGE:
                G_next = self._prune_edge(G_next, observation, parameters)

            else:
                span.set_attribute("rae.outcome.label", "fail")
                raise ValueError(f"Unknown action type: {action_type}")

            # Update timestamp
            G_next.last_updated = datetime.now()

            nodes_delta = len(G_next.nodes) - len(graph.nodes)
            edges_delta = len(G_next.edges) - len(graph.edges)

            span.set_attribute("rae.graph.nodes_after", len(G_next.nodes))
            span.set_attribute("rae.graph.edges_after", len(G_next.edges))
            span.set_attribute("rae.graph.nodes_delta", nodes_delta)
            span.set_attribute("rae.graph.edges_delta", edges_delta)
            span.set_attribute("rae.outcome.label", "success")

            logger.info(
                "graph_transformation_completed",
                action_type=action_type.value,
                nodes_after=len(G_next.nodes),
                edges_after=len(G_next.edges),
                nodes_delta=nodes_delta,
                edges_delta=edges_delta,
            )

            return G_next

    def _add_node(
        self,
        graph: KnowledgeGraph,
        observation: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> KnowledgeGraph:
        """
        Add new node to graph.

        Ensures no duplicate nodes with same label.

        Args:
            graph: Current graph
            observation: Must contain "node_data" with node information
            parameters: Optional parameters

        Returns:
            Updated graph
        """
        node_data = observation.get("node_data") or parameters.get("node_data")

        if not node_data:
            logger.warning("add_node_missing_data")
            return graph

        # Check for duplicates
        existing = self._find_duplicate_node(graph, node_data["label"])
        if existing:
            logger.info(
                "node_already_exists", node_id=existing.id, label=existing.label
            )
            return graph

        # Create new node
        node = GraphNode(
            id=node_data.get("id", f"node_{len(graph.nodes)}"),
            label=node_data["label"],
            node_type=node_data.get("node_type", "entity"),
            properties=node_data.get("properties", {}),
            created_at=datetime.now(),
            last_updated=datetime.now(),
            importance=node_data.get("importance", 0.5),
            centrality=0.0,  # Will be computed later
        )

        graph.nodes[node.id] = node

        logger.debug("node_added", node_id=node.id, label=node.label)

        return graph

    def _add_edge(
        self,
        graph: KnowledgeGraph,
        observation: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> KnowledgeGraph:
        """
        Add or strengthen edge.

        If edge already exists, increase weight and evidence count.
        Otherwise, create new edge.

        Args:
            graph: Current graph
            observation: Must contain "edge_data" with edge information
            parameters: Optional parameters

        Returns:
            Updated graph
        """
        edge_data = observation.get("edge_data") or parameters.get("edge_data")

        if not edge_data:
            logger.warning("add_edge_missing_data")
            return graph

        source_id = edge_data["source_id"]
        target_id = edge_data["target_id"]
        relation = edge_data["relation"]

        # Check nodes exist
        if source_id not in graph.nodes or target_id not in graph.nodes:
            logger.warning("edge_nodes_not_found", source=source_id, target=target_id)
            return graph

        # Check if edge already exists
        edge_id = f"{source_id}_{relation}_{target_id}"
        existing_edge = graph.edges.get(edge_id)

        if existing_edge:
            # Strengthen existing edge
            existing_edge.weight = min(1.0, existing_edge.weight + 0.1)
            existing_edge.evidence_count += 1
            existing_edge.last_updated = datetime.now()

            logger.debug(
                "edge_strengthened",
                edge_id=edge_id,
                new_weight=existing_edge.weight,
                evidence_count=existing_edge.evidence_count,
            )
        else:
            # Create new edge
            edge = GraphEdge(
                id=edge_id,
                source_id=source_id,
                target_id=target_id,
                relation=relation,
                weight=edge_data.get("weight", 0.7),
                confidence=edge_data.get("confidence", 0.8),
                created_at=datetime.now(),
                last_updated=datetime.now(),
                evidence_count=1,
            )

            graph.edges[edge_id] = edge

            logger.debug("edge_added", edge_id=edge_id, weight=edge.weight)

        return graph

    def _update_edge_weight(
        self,
        graph: KnowledgeGraph,
        observation: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> KnowledgeGraph:
        """
        Update edge weights with temporal decay.

        Mathematical formulation:
          w(t) = w(t_0) * exp(-Δt / half_life)

        Where:
          - w(t): Weight at time t
          - w(t_0): Weight at last update
          - Δt: Time since last update
          - half_life: Edge half-life parameter

        Args:
            graph: Current graph
            observation: Optional observation data
            parameters: Optional parameters

        Returns:
            Updated graph with decayed edge weights
        """
        now = datetime.now()

        edges_to_remove = []

        for edge_id, edge in graph.edges.items():
            # Temporal decay: w(t) = w(t_0) * exp(-Δt / half_life)
            time_delta_days = (now - edge.last_updated).total_seconds() / 86400
            decay = np.exp(-time_delta_days / self.edge_half_life_days)

            # Apply decay
            edge.weight = edge.weight * decay

            # Mark for pruning if below threshold
            if edge.weight < self.edge_prune_threshold:
                edges_to_remove.append(edge_id)

        # Remove pruned edges
        for edge_id in edges_to_remove:
            del graph.edges[edge_id]
            logger.debug("edge_pruned_by_decay", edge_id=edge_id)

        logger.info(
            "edge_weights_updated",
            edges_total=len(graph.edges),
            edges_pruned=len(edges_to_remove),
        )

        return graph

    def _merge_nodes(
        self,
        graph: KnowledgeGraph,
        observation: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> KnowledgeGraph:
        """
        Merge duplicate nodes (entity resolution).

        Merges node2 into node1:
          - Properties are merged
          - Importance is maximized
          - All edges from/to node2 are redirected to node1

        Args:
            graph: Current graph
            observation: Optional observation data
            parameters: Must contain "node1_id" and "node2_id"

        Returns:
            Updated graph with merged nodes
        """
        node1_id = parameters.get("node1_id")
        node2_id = parameters.get("node2_id")

        if not node1_id or not node2_id:
            logger.warning("merge_nodes_missing_ids")
            return graph

        node1 = graph.nodes.get(node1_id)
        node2 = graph.nodes.get(node2_id)

        if not node1 or not node2:
            logger.warning("merge_nodes_not_found")
            return graph

        # Create merged node (keep node1, merge properties)
        node1.properties.update(node2.properties)
        node1.importance = max(node1.importance, node2.importance)
        node1.last_updated = datetime.now()

        # Remove node2
        del graph.nodes[node2_id]

        # Redirect all edges from node2 to node1
        edges_to_update = []
        for edge_id, edge in graph.edges.items():
            if edge.source_id == node2_id:
                edges_to_update.append((edge_id, "source"))
            elif edge.target_id == node2_id:
                edges_to_update.append((edge_id, "target"))

        for edge_id, direction in edges_to_update:
            edge = graph.edges[edge_id]

            # Create new edge ID
            if direction == "source":
                new_edge_id = f"{node1_id}_{edge.relation}_{edge.target_id}"
            else:
                new_edge_id = f"{edge.source_id}_{edge.relation}_{node1_id}"

            # Check if edge already exists
            if new_edge_id in graph.edges:
                # Merge weights
                existing = graph.edges[new_edge_id]
                existing.weight = min(1.0, existing.weight + edge.weight)
                existing.evidence_count += edge.evidence_count
            else:
                # Update edge
                if direction == "source":
                    edge.source_id = node1_id
                else:
                    edge.target_id = node1_id

                edge.id = new_edge_id
                graph.edges[new_edge_id] = edge

            # Remove old edge
            if edge_id != new_edge_id:
                del graph.edges[edge_id]

        logger.info(
            "nodes_merged",
            node1=node1_id,
            node2=node2_id,
            edges_redirected=len(edges_to_update),
        )

        return graph

    def _prune_node(
        self,
        graph: KnowledgeGraph,
        observation: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> KnowledgeGraph:
        """
        Remove low-value node.

        Also removes all edges connected to this node.

        Args:
            graph: Current graph
            observation: Optional observation data
            parameters: Must contain "node_id"

        Returns:
            Updated graph with node removed
        """
        node_id = parameters.get("node_id")

        if not node_id or node_id not in graph.nodes:
            logger.warning("prune_node_not_found", node_id=node_id)
            return graph

        # Remove node
        del graph.nodes[node_id]

        # Remove all edges connected to this node
        edges_to_remove = [
            edge_id
            for edge_id, edge in graph.edges.items()
            if edge.source_id == node_id or edge.target_id == node_id
        ]

        for edge_id in edges_to_remove:
            del graph.edges[edge_id]

        logger.info(
            "node_pruned",
            node_id=node_id,
            edges_removed=len(edges_to_remove),
        )

        return graph

    def _prune_edge(
        self,
        graph: KnowledgeGraph,
        observation: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> KnowledgeGraph:
        """
        Remove specific edge.

        Args:
            graph: Current graph
            observation: Optional observation data
            parameters: Must contain "edge_id"

        Returns:
            Updated graph with edge removed
        """
        edge_id = parameters.get("edge_id")

        if not edge_id or edge_id not in graph.edges:
            logger.warning("prune_edge_not_found", edge_id=edge_id)
            return graph

        del graph.edges[edge_id]

        logger.debug("edge_pruned", edge_id=edge_id)

        return graph

    def _find_duplicate_node(
        self,
        graph: KnowledgeGraph,
        label: str,
        similarity_threshold: Optional[float] = None,
    ) -> Optional[GraphNode]:
        """
        Find node with similar label (for duplicate detection).

        Currently uses exact string matching (case-insensitive).
        Future: Use embedding similarity for semantic matching.

        Args:
            graph: Current graph
            label: Node label to search for
            similarity_threshold: Optional similarity threshold (reserved for future use)

        Returns:
            Duplicate node if found, None otherwise
        """
        # Simple exact match for now
        # TODO: Use embedding similarity for semantic matching with similarity_threshold
        for node in graph.nodes.values():
            if node.label.lower() == label.lower():
                return node

        return None

    def analyze_convergence(
        self, graph_history: List[KnowledgeGraph]
    ) -> Dict[str, Any]:
        """
        Analyze whether graph is converging to stable structure.

        Convergence metrics:
          1. Node churn rate: Avg additions/deletions per timestep
          2. Edge churn rate: Avg additions/deletions per timestep
          3. Spectral gap: λ_1 - λ_2 from adjacency matrix eigenvalues
          4. Clustering coefficient variance

        Convergence criteria:
          - Node churn < 5 per timestep
          - Edge churn < 10 per timestep
          - Spectral gap < 0.5

        Args:
            graph_history: List of graph snapshots over time

        Returns:
            Dictionary with convergence metrics and is_converging flag
        """
        with tracer.start_as_current_span("rae.graph.analyze_convergence") as span:
            span.set_attribute("rae.graph.history_length", len(graph_history))

            if len(graph_history) < 2:
                span.set_attribute(
                    "rae.graph.convergence_result", "insufficient_history"
                )
                span.set_attribute("rae.outcome.label", "fail")
                return {
                    "is_converging": False,
                    "reason": "insufficient_history",
                    "history_length": len(graph_history),
                }

            # Node churn
            node_counts = [len(g.nodes) for g in graph_history]
            node_deltas = [
                abs(node_counts[i + 1] - node_counts[i])
                for i in range(len(node_counts) - 1)
            ]
            node_churn = float(np.mean(node_deltas)) if node_deltas else 0.0
            span.set_attribute("rae.graph.node_churn", node_churn)

            # Edge churn
            edge_counts = [len(g.edges) for g in graph_history]
            edge_deltas = [
                abs(edge_counts[i + 1] - edge_counts[i])
                for i in range(len(edge_counts) - 1)
            ]
            edge_churn = float(np.mean(edge_deltas)) if edge_deltas else 0.0
            span.set_attribute("rae.graph.edge_churn", edge_churn)

            # Spectral gap (from latest graph)
            latest_graph = graph_history[-1]
            spectral_gap = 0.0

            span.set_attribute("rae.tenant_id", latest_graph.tenant_id)
            span.set_attribute("rae.project_id", latest_graph.project_id)
            span.set_attribute("rae.graph.node_count", len(latest_graph.nodes))
            span.set_attribute("rae.graph.edge_count", len(latest_graph.edges))

            if len(latest_graph.nodes) > 1:
                adj_matrix = latest_graph.adjacency_matrix()

                if adj_matrix.size > 0:
                    try:
                        eigenvalues = np.linalg.eigvals(adj_matrix)
                        eigenvalues_sorted = np.sort(np.abs(eigenvalues))[::-1]

                        if len(eigenvalues_sorted) >= 2:
                            spectral_gap = float(
                                eigenvalues_sorted[0] - eigenvalues_sorted[1]
                            )
                            span.set_attribute(
                                "rae.graph.eigenvalue_1", float(eigenvalues_sorted[0])
                            )
                            span.set_attribute(
                                "rae.graph.eigenvalue_2", float(eigenvalues_sorted[1])
                            )
                    except Exception as e:
                        logger.warning("spectral_gap_computation_failed", error=str(e))
                        spectral_gap = 0.0

            span.set_attribute("rae.graph.spectral_gap", spectral_gap)

            # Convergence criteria
            # For true convergence, we want very low churn (approaching stability)
            is_converging = (
                node_churn < 1.0  # Less than 1 node added/removed per step
                and edge_churn < 2.0  # Less than 2 edges added/removed per step
                and spectral_gap < 0.5  # Stable eigenvalue spectrum
            )

            span.set_attribute("rae.graph.is_converging", is_converging)
            span.set_attribute(
                "rae.outcome.label", "success" if is_converging else "not_converged"
            )

            return {
                "is_converging": is_converging,
                "node_churn": node_churn,
                "edge_churn": edge_churn,
                "spectral_gap": spectral_gap,
                "node_count": len(latest_graph.nodes),
                "edge_count": len(latest_graph.edges),
                "history_length": len(graph_history),
            }
