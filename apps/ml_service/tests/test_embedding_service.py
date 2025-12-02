from unittest.mock import MagicMock, patch

import pytest

from apps.ml_service.services.embedding_service import EmbeddingMLService


# Mock SentenceTransformer at the module level
@pytest.fixture(autouse=True)
def mock_sentence_transformer_class():
    with patch(
        "apps.ml_service.services.embedding_service.SentenceTransformer"
    ) as mock_st_class:
        mock_st_instance = MagicMock()
        mock_st_class.return_value = mock_st_instance
        # Configure mock_st_instance for methods used by EmbeddingMLService

        # Mock objects that have a .tolist() method for encode return value
        mock_np_array1 = MagicMock()
        mock_np_array1.tolist.return_value = [0.1, 0.2]
        mock_np_array2 = MagicMock()
        mock_np_array2.tolist.return_value = [0.3, 0.4]

        mock_st_instance.encode.return_value = [mock_np_array1, mock_np_array2]
        mock_st_instance.get_sentence_embedding_dimension.return_value = 2
        yield mock_st_class


@pytest.fixture
def embedding_service():
    # Ensure a fresh instance for each test to properly test singleton behavior
    # by resetting the internal state of the singleton
    EmbeddingMLService._instance = None
    EmbeddingMLService._model = None
    service = EmbeddingMLService(model_name="test-model")
    yield service
    # Clean up after test
    EmbeddingMLService._instance = None
    EmbeddingMLService._model = None


def test_embedding_service_init_loads_model(
    embedding_service, mock_sentence_transformer_class
):
    """Test that the SentenceTransformer model is loaded on initialization."""
    mock_sentence_transformer_class.assert_called_once_with("test-model")
    assert embedding_service._model is not None


def test_embedding_service_singleton_behavior(mock_sentence_transformer_class):
    """Test that only one instance of SentenceTransformer is loaded due to singleton pattern."""
    EmbeddingMLService._instance = None
    EmbeddingMLService._model = None
    service1 = EmbeddingMLService(model_name="model-a")
    service2 = EmbeddingMLService(model_name="model-b")

    assert service1 is service2
    # SentenceTransformer class's __init__ should only be called once, for the first model_name
    mock_sentence_transformer_class.assert_called_once_with("model-a")


def test_generate_embeddings_single_text(
    embedding_service, mock_sentence_transformer_class
):
    """Test generating embeddings for a single text."""
    texts = ["hello world"]

    mock_np_array_single = MagicMock()
    mock_np_array_single.tolist.return_value = [0.1, 0.2]
    mock_sentence_transformer_class.return_value.encode.return_value = [
        mock_np_array_single
    ]

    embeddings = embedding_service.generate_embeddings(texts)
    embedding_service._model.encode.assert_called_once_with(
        texts, show_progress_bar=False
    )
    assert embeddings == [[0.1, 0.2]]


def test_generate_embeddings_multiple_texts(
    embedding_service, mock_sentence_transformer_class
):
    """Test generating embeddings for multiple texts."""
    texts = ["hello world", "foo bar"]

    mock_np_array1 = MagicMock()
    mock_np_array1.tolist.return_value = [0.1, 0.2]
    mock_np_array2 = MagicMock()
    mock_np_array2.tolist.return_value = [0.3, 0.4]
    mock_sentence_transformer_class.return_value.encode.return_value = [
        mock_np_array1,
        mock_np_array2,
    ]

    embeddings = embedding_service.generate_embeddings(texts)
    embedding_service._model.encode.assert_called_once_with(
        texts, show_progress_bar=False
    )
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]


def test_generate_embeddings_empty_list(embedding_service):
    """Test generating embeddings for an empty list of texts."""
    embeddings = embedding_service.generate_embeddings([])
    assert embeddings == []
    embedding_service._model.encode.assert_not_called()


def test_get_embedding_dimension(embedding_service, mock_sentence_transformer_class):
    """Test getting the embedding dimension."""
    expected_dimension = 2
    mock_sentence_transformer_class.return_value.get_sentence_embedding_dimension.return_value = (
        expected_dimension
    )

    dimension = embedding_service.get_embedding_dimension()
    embedding_service._model.get_sentence_embedding_dimension.assert_called_once()
    assert dimension == expected_dimension
