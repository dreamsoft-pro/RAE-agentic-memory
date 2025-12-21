from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from apps.ml_service.services.entity_resolution import (
    EntityResolutionMLService,
    get_embedding_model,
)


# Fixture to provide a mocked SentenceTransformer instance
@pytest.fixture
def mock_sentence_transformer_instance():
    mock_st_instance = MagicMock()
    # Configure default behaviors for the mock instance methods
    mock_st_instance.encode.return_value = np.array(
        [[0.1, 0.2]]
    )  # Default, can be overridden
    mock_st_instance.get_sentence_embedding_dimension.return_value = 2
    yield mock_st_instance


# Fixture to mock sklearn components (AgglomerativeClustering and cosine_similarity)
@pytest.fixture
def mock_sklearn_components():
    with (
        patch(
            "apps.ml_service.services.entity_resolution.AgglomerativeClustering"
        ) as MockAgglomerativeClustering,
        patch(
            "apps.ml_service.services.entity_resolution.cosine_similarity"
        ) as MockCosineSimilarity,
    ):
        mock_agg_instance = MagicMock()
        MockAgglomerativeClustering.return_value = mock_agg_instance

        yield MockAgglomerativeClustering, mock_agg_instance, MockCosineSimilarity


@pytest.fixture
def entity_resolution_service(mock_sentence_transformer_instance):
    # Patch get_embedding_model to return our specific mock instance
    with patch(
        "apps.ml_service.services.entity_resolution.get_embedding_model",
        return_value=mock_sentence_transformer_instance,
    ):
        # Ensure get_embedding_model's internal singleton cache is cleared for isolation
        get_embedding_model._EMBEDDING_MODEL = None

        service = EntityResolutionMLService(similarity_threshold=0.8)
        yield service

        # Clean up after test
        get_embedding_model._EMBEDDING_MODEL = None


def test_entity_resolution_init(
    entity_resolution_service, mock_sentence_transformer_instance
):
    """Test EntityResolutionMLService initialization."""
    assert entity_resolution_service.similarity_threshold == 0.8
    assert (
        entity_resolution_service.model is mock_sentence_transformer_instance
    )  # Ensure it uses our mock
    # get_embedding_model is patched, so SentenceTransformer itself isn't directly called here
    # We check that get_embedding_model returned our mock instance


def test_resolve_entities_empty_nodes(
    entity_resolution_service, mock_sentence_transformer_instance
):
    """Test resolving entities with an empty list of nodes."""
    merge_groups, statistics = entity_resolution_service.resolve_entities([])
    assert merge_groups == []
    assert statistics["nodes_processed"] == 0
    assert statistics["groups_found"] == 0
    assert statistics["reason"] == "insufficient_nodes"
    mock_sentence_transformer_instance.encode.assert_not_called()


def test_resolve_entities_single_node(
    entity_resolution_service, mock_sentence_transformer_instance
):
    """Test resolving entities with a single node."""
    nodes = [{"id": "node1", "label": "label1"}]
    merge_groups, statistics = entity_resolution_service.resolve_entities(nodes)
    assert merge_groups == []
    assert statistics["nodes_processed"] == 1
    assert statistics["groups_found"] == 0
    assert statistics["reason"] == "insufficient_nodes"
    mock_sentence_transformer_instance.encode.assert_not_called()


def test_resolve_entities_multiple_nodes_mocked_clustering(
    entity_resolution_service,
    mock_sklearn_components,
    mock_sentence_transformer_instance,
):
    """Test resolving entities with multiple nodes and mocked clustering."""
    (
        MockAgglomerativeClustering,
        mock_agg_instance,
        MockCosineSimilarity,
    ) = mock_sklearn_components

    nodes = [
        {"id": "node1", "label": "apple"},
        {"id": "node2", "label": "orange"},
        {"id": "node3", "label": "banana"},
        {"id": "node4", "label": "grape"},
    ]
    node_labels = [node["label"] for node in nodes]

    # Configure SentenceTransformer.encode for this specific test
    mock_sentence_transformer_instance.encode.return_value = np.array(
        [
            [0.1, 0.2],  # apple
            [0.11, 0.21],  # orange (similar to apple)
            [0.9, 0.8],  # banana
            [0.91, 0.81],  # grape (similar to banana)
        ]
    )

    # Configure AgglomerativeClustering to create two clusters for 4 nodes
    mock_agg_instance.fit_predict.return_value = np.array([0, 0, 1, 1])

    # Configure cosine_similarity for _calculate_min_similarity calls
    MockCosineSimilarity.side_effect = [
        np.array([[0.95]]),  # sim(apple, orange)
        np.array([[0.92]]),  # sim(banana, grape)
    ]

    merge_groups, statistics = entity_resolution_service.resolve_entities(nodes)

    assert len(merge_groups) == 2
    assert sorted(merge_groups[0]) == sorted(["node1", "node2"])  # Order might vary
    assert sorted(merge_groups[1]) == sorted(["node3", "node4"])
    assert statistics["nodes_processed"] == 4
    assert statistics["groups_found"] == 2
    assert statistics["similarity_threshold"] == 0.8

    mock_sentence_transformer_instance.encode.assert_called_once_with(node_labels)
    MockAgglomerativeClustering.assert_called_once()
    mock_agg_instance.fit_predict.assert_called_once()
    assert MockCosineSimilarity.call_count == 2  # Called twice, once for each cluster


def test_resolve_entities_override_threshold(
    entity_resolution_service,
    mock_sklearn_components,
    mock_sentence_transformer_instance,
):
    """Test resolving entities with an overridden similarity threshold."""
    (
        MockAgglomerativeClustering,
        mock_agg_instance,
        MockCosineSimilarity,
    ) = mock_sklearn_components

    nodes = [
        {"id": "node1", "label": "apple"},
        {"id": "node2", "label": "orange"},
    ]
    node_labels = [node["label"] for node in nodes]

    mock_sentence_transformer_instance.encode.return_value = np.array(
        [[0.1, 0.2], [0.11, 0.21]]
    )

    # Configure AgglomerativeClustering to create one cluster for 2 nodes
    mock_agg_instance.fit_predict.return_value = np.array([0, 0])
    MockCosineSimilarity.return_value = np.array([[0.95]])  # for single pair

    entity_resolution_service.resolve_entities(nodes, similarity_threshold=0.9)

    # Ensure clustering uses the overridden threshold
    MockAgglomerativeClustering.assert_called_once_with(
        n_clusters=None,
        metric="cosine",
        linkage="average",
        distance_threshold=pytest.approx(
            0.1
        ),  # 1 - 0.9. Using pytest.approx for float comparison
    )
    mock_sentence_transformer_instance.encode.assert_called_once_with(node_labels)
    mock_agg_instance.fit_predict.assert_called_once()


def test_calculate_min_similarity(entity_resolution_service, mock_sklearn_components):
    """Test the private helper method _calculate_min_similarity."""
    _, _, MockCosineSimilarity = mock_sklearn_components

    embeddings = [np.array([0.1, 0.2]), np.array([0.15, 0.25]), np.array([0.9, 0.8])]
    # Mock cosine_similarity for specific return values
    MockCosineSimilarity.side_effect = [
        np.array([[0.9]]),  # sim(0,1)
        np.array([[0.2]]),  # sim(0,2)
        np.array([[0.3]]),  # sim(1,2)
    ]
    min_sim = entity_resolution_service._calculate_min_similarity(embeddings)
    assert min_sim == 0.2  # Smallest of 0.9, 0.2, 0.3
    # Called for (0,1), (0,2), (1,2) - total 3 times
    assert MockCosineSimilarity.call_count == 3


def test_calculate_similarity_matrix(
    entity_resolution_service,
    mock_sentence_transformer_instance,
    mock_sklearn_components,
):
    """Test calculate_similarity_matrix method."""
    _, _, MockCosineSimilarity = mock_sklearn_components

    labels = ["cat", "dog", "bird"]
    expected_embeddings_np = np.array([[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]])
    mock_sentence_transformer_instance.encode.return_value = expected_embeddings_np

    expected_sim_matrix = np.array([[1.0, 0.9, 0.8], [0.9, 1.0, 0.7], [0.8, 0.7, 1.0]])
    MockCosineSimilarity.return_value = (
        expected_sim_matrix  # mock cosine_similarity for this function
    )

    similarity_matrix = entity_resolution_service.calculate_similarity_matrix(labels)

    mock_sentence_transformer_instance.encode.assert_called_once_with(labels)
    MockCosineSimilarity.assert_called_once_with(expected_embeddings_np)
    assert np.array_equal(similarity_matrix, expected_sim_matrix)
