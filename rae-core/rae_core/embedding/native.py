"""Native Embedding Provider using ONNX Runtime.

This provider runs embedding models locally using ONNX Runtime, ensuring
consistent, high-performance vector generation across platforms (Linux, Windows, Mobile).
"""

from pathlib import Path

import numpy as np

try:
    import onnxruntime as ort
    from tokenizers import Tokenizer
except ImportError:
    ort = None
    Tokenizer = None

from rae_core.interfaces.embedding import IEmbeddingProvider


class NativeEmbeddingProvider(IEmbeddingProvider):
    """Embedding provider using local ONNX models."""

    def __init__(
        self,
        model_path: str | Path,
        tokenizer_path: str | Path,
        model_name: str = "nomic-embed-text-v1.5",
        max_length: int = 8192,
        normalize: bool = True,
        matryoshka_dim: int | None = None,
    ):
        """Initialize ONNX provider.

        Args:
            model_path: Path to .onnx model file.
            tokenizer_path: Path to tokenizer.json file.
            model_name: Name of the model.
            max_length: Maximum sequence length.
            normalize: Whether to L2-normalize vectors.
            matryoshka_dim: Optional dimension to truncate to (e.g. 256).
        """
        if ort is None or Tokenizer is None:
            raise ImportError(
                "onnxruntime and tokenizers are required. "
                "Install with: pip install onnxruntime tokenizers"
            )

        self.model_path = str(model_path)
        self.tokenizer_path = str(tokenizer_path)
        self.model_name = model_name
        self.max_length = max_length
        self.normalize = normalize
        self.matryoshka_dim = matryoshka_dim

        # Load Tokenizer
        self.tokenizer = Tokenizer.from_file(self.tokenizer_path)
        if self.tokenizer.padding is None:
            self.tokenizer.enable_padding(length=max_length)
        if self.tokenizer.truncation is None:
            self.tokenizer.enable_truncation(max_length=max_length)

        # Load ONNX Model
        # Use CUDA if available, else CPU
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        if "CUDAExecutionProvider" not in ort.get_available_providers():
            providers = ["CPUExecutionProvider"]

        self.session = ort.InferenceSession(self.model_path, providers=providers)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name # Usually 'last_hidden_state'

    def get_dimension(self) -> int:
        """Return embedding dimension."""
        if self.matryoshka_dim:
            return self.matryoshka_dim
        # Infer from model output shape (batch, seq, dim) or (batch, dim)
        # We can run a dummy inference or trust config.
        # For nomic-embed-text v1.5 it is 768.
        return 768

    def _mean_pooling(self, last_hidden_state: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        """Perform Mean Pooling on last hidden state."""
        # last_hidden_state: (batch, seq, dim)
        # attention_mask: (batch, seq)

        # Expand mask to (batch, seq, dim)
        mask_expanded = np.expand_dims(attention_mask, axis=-1).astype(last_hidden_state.dtype)

        # Sum embeddings (ignoring padding)
        sum_embeddings = np.sum(last_hidden_state * mask_expanded, axis=1)

        # Sum mask (count of tokens)
        sum_mask = np.sum(mask_expanded, axis=1)
        sum_mask = np.clip(sum_mask, a_min=1e-9, a_max=None) # Avoid div by zero

        return sum_embeddings / sum_mask

    def _normalize_l2(self, vectors: np.ndarray) -> np.ndarray:
        """Perform L2 normalization."""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.clip(norms, a_min=1e-9, a_max=None)

    async def embed_text(self, text: str) -> list[float]:
        """Embed a single text string."""
        vectors = await self.embed_batch([text])
        return vectors[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts."""
        # 1. Tokenize
        encoded = self.tokenizer.encode_batch(texts)

        # Prepare inputs for ONNX
        input_ids = np.array([e.ids for e in encoded], dtype=np.int64)
        attention_mask = np.array([e.attention_mask for e in encoded], dtype=np.int64)

        # Some models require token_type_ids, Nomic usually doesn't or handles it.
        # If model expects it, we need to provide it.
        # Nomic ONNX usually takes: input_ids, attention_mask.

        inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        }

        # Check if model needs token_type_ids
        input_names = [i.name for i in self.session.get_inputs()]
        if "token_type_ids" in input_names:
             inputs["token_type_ids"] = np.array([e.type_ids for e in encoded], dtype=np.int64)

        # 2. Run Inference
        outputs = self.session.run(None, inputs)

        # Output is typically last_hidden_state (batch, seq, dim)
        last_hidden_state = outputs[0]

        # 3. Pooling (Mean)
        embeddings = self._mean_pooling(last_hidden_state, attention_mask)

        # 4. Matryoshka Truncation (Optional)
        if self.matryoshka_dim:
            embeddings = embeddings[:, :self.matryoshka_dim]

        # 5. Normalization (L2)
        if self.normalize:
            embeddings = self._normalize_l2(embeddings)

        return embeddings.tolist()
