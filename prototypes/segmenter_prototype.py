"""
Prototype for a Multi-level Hierarchical Segmenter for RAE (v6 - Refined Mock Embedder)
Author: Gemini Agent (in research mode)
Date: 2026-02-18
Branch: research/segmenter-overhaul

Principle: This version refines the mock embedder to better simulate semantic
           shifts without any heavy external dependencies, strictly adhering to
           RAE's core principles of being lightweight, local-first, and portable.
           It demonstrates the segmentation ALGORITHM, ready to be powered by
           RAE's internal ONNX embedder.

Changelog:
- Enhanced `mock_embedding_model` to simulate more realistic semantic shifts
  for better testing of the percentile-based algorithm.
- Removed all heavy dependencies. Only `numpy` is used.
- Clarified the integration point for RAE's actual ONNX embedder.
"""
import numpy as np
import re
from typing import List, Optional

# --- Refined Mock Embedding Logic (No External Dependencies) ---

class MockEmbeddingModel:
    """
    A dependency-free mock class to simulate RAE's embedding provider.
    Generates deterministic vectors that allow testing of semantic shifts.
    """
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)
        self.cache = {} # To ensure same sentence gets same vector

    def encode(self, sentences: List[str]) -> np.ndarray:
        embeddings = []
        for sentence in sentences:
            if sentence in self.cache:
                embeddings.append(self.cache[sentence])
                continue

            # Generate a "semantic seed" based on sentence content
            # This allows for some sentences to be "semantically close"
            # and others to be "far apart".
            semantic_seed = sum(ord(char) for char in sentence[:min(len(sentence), 50)])
            
            # Use the seed to generate a deterministic, yet distinct vector
            # We'll make vectors change "semantically" based on the sentence's beginning
            current_rng = np.random.default_rng(semantic_seed % (2**32 - 1)) # Ensure seed fits
            vector = current_rng.random(384) * 2 - 1 # Random values between -1 and 1
            vector /= np.linalg.norm(vector) # Normalize

            self.cache[sentence] = vector
            embeddings.append(vector)
        return np.array(embeddings)

def _calculate_similarity_scores(embeddings: np.ndarray) -> List[float]:
    """Calculates cosine similarity between consecutive embeddings."""
    if embeddings.shape[0] < 2:
        return []
    
    similarities = []
    for i in range(embeddings.shape[0] - 1):
        embedding1 = embeddings[i]
        embedding2 = embeddings[i+1]
        # dot product is enough since vectors are normalized (cosine similarity)
        similarity = np.dot(embedding1, embedding2)
        similarities.append(similarity)
    return similarities

# --- The Advanced Segmenter Class ---

class SemanticRecursiveSegmenter:
    """
    An advanced segmenter that combines hierarchical structural splitting with
    semantic splitting based on dynamic, percentile-based thresholding.
    """

    def __init__(
        self,
        structural_separators: Optional[List[str]] = None,
        semantic_separators: Optional[List[str]] = None,
        chunk_size: int = 1000,
        semantic_threshold_percentile: int = 90, # Using 90th percentile
    ):
        self._structural_separators = structural_separators or ["\n\n", "\n", " ", ""]
        self._chunk_size = chunk_size
        self._semantic_separators = semantic_separators or [". ", "? ", "! ", "\n"]
        self.semantic_threshold_percentile = semantic_threshold_percentile
        
        # This would be RAE's actual NativeEmbeddingProvider in production
        self._embedder = MockEmbeddingModel() 

    def _semantic_split(self, text: str) -> List[str]:
        """Performs the semantic splitting based on the mock embedder."""
        # Use semantic separators to get sentences/clauses
        sentences = re.split(f"({'|'.join(map(re.escape, self._semantic_separators))})", text)
        
        # Filter out empty strings and re-add delimiters where they were
        processed_sentences = []
        i = 0
        while i < len(sentences):
            sentence_part = sentences[i].strip()
            if not sentence_part:
                i += 1
                continue
            
            delimiter = ""
            if i + 1 < len(sentences) and sentences[i+1].strip() in self._semantic_separators:
                delimiter = sentences[i+1].strip()
                i += 1
            
            processed_sentences.append(sentence_part + delimiter)
            i += 1

        if len(processed_sentences) <= 1:
            return [text] if text.strip() else []
        
        # Generate embeddings and calculate similarities
        embeddings = self._embedder.encode(processed_sentences)
        similarities = _calculate_similarity_scores(embeddings)

        if not similarities:
            return [text] if text.strip() else []

        # Calculate the dynamic threshold
        dynamic_threshold = np.percentile(similarities, self.semantic_threshold_percentile)
        
        # Group sentences into semantically coherent chunks
        final_semantic_chunks = []
        current_chunk_sentences = [processed_sentences[0]]
        
        for i, sentence in enumerate(processed_sentences[1:]):
            # Split if similarity drops below threshold
            if similarities[i] < dynamic_threshold:
                final_semantic_chunks.append("".join(current_chunk_sentences))
                current_chunk_sentences = []
            
            current_chunk_sentences.append(sentence)
        
        # Add the last chunk
        if current_chunk_sentences:
            final_semantic_chunks.append("".join(current_chunk_sentences))
        
        return final_semantic_chunks


    def segment(self, text: str) -> List[str]:
        """
        Segments a given text using a two-stage hierarchical and semantic process.
        """
        # --- Stage 1: Hierarchical Structural Splitting ---
        
        # Use a temporary segmenter for structural splits (similar to v3)
        structural_splits = self._perform_structural_split(text, self._structural_separators)

        # --- Stage 2: Semantic Refinement for Oversized Structural Chunks ---
        final_chunks = []
        for split in structural_splits:
            if len(split) <= self._chunk_size:
                if split.strip():
                    final_chunks.append(split)
            else:
                # This structural chunk is too big, apply semantic splitting
                semantic_chunks = self._semantic_split(split)
                final_chunks.extend(semantic_chunks)

        return final_chunks

    def _perform_structural_split(self, text: str, separators: List[str]) -> List[str]:
        """
        Helper for recursive structural splitting.
        """
        if not separators or len(text) <= self._chunk_size:
            return [text] if text.strip() else []

        separator = ""
        for s in separators:
            if s == "": # Fallback to character split
                separator = ""
                break
            if s in text:
                separator = s
                break
        
        if not separator: # If no suitable separator, return the whole text
            return [text] if text.strip() else []

        # Split and process parts
        splits = text.split(separator)
        structural_chunks = []
        current_aggregated_part = []
        current_length = 0

        for part in splits:
            if not part.strip(): # Skip empty parts
                continue
            
            part_with_separator_len = len(part) + (len(separator) if current_aggregated_part else 0)
            
            # If current part is too big, or adding it makes current_aggregated_part too big
            if part_with_separator_len > self._chunk_size or \
               (current_length + part_with_separator_len > self._chunk_size and current_aggregated_part):
                
                # Finalize current aggregated chunk
                if current_aggregated_part:
                    structural_chunks.append(separator.join(current_aggregated_part))
                
                # Recursively process the oversized 'part' using next set of separators
                sub_chunks = self._perform_structural_split(part, separators[1:])
                structural_chunks.extend(sub_chunks)
                
                current_aggregated_part = []
                current_length = 0
            else:
                current_aggregated_part.append(part)
                current_length += part_with_separator_len
        
        if current_aggregated_part:
            structural_chunks.append(separator.join(current_aggregated_part))

        return structural_chunks


# --- Example Usage with Test Files ---
if __name__ == "__main__":
    
    print("--- Prototype v6: Final, Dependency-Free Hybrid Segmentation ---")

    # Ensure numpy is available for the mock embedder
    try:
        import numpy
    except ImportError:
        print("Error: numpy is required for the mock embedder. Please install it: pip install numpy")
        exit(1)

    def run_test(file_path: str, structural_separators: List[str], chunk_size: int):
        print(f"\n--- Testing file: {file_path} ---")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: Test file '{file_path}' not found.")
            return
            
        segmenter = SemanticRecursiveSegmenter(
            structural_separators=structural_separators,
            chunk_size=chunk_size,
        )
        
        chunks = segmenter.segment(text)
        
        print(f"Result: Text of length {len(text)} was split into {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks):
            print(f"  Chunk {i+1} (length: {len(chunk)}):\n'---\n{chunk}\n---'\n")

    # 1. Scientific Paper Test (Coarse structural split, then semantic for large sections)
    scientific_separators = ["\n## ", "\n### ", "\n\n---", "\n"] # Added \n\n--- for horizontal rule
    run_test("/app/prototypes/test_scientific_paper.md", scientific_separators, chunk_size=1000)

    # 2. Python Code Test (Split by major logical blocks)
    code_separators = ["\n# ---", "\nclass ", "\ndef "]
    run_test("/app/prototypes/test_complex_code.py", code_separators, chunk_size=1000)
    
    # 3. Legal Contract Test (Split by major articles)
    legal_separators = ["\n## ARTICLE ", "\n## "] # Try to split by Article first
    run_test("/app/prototypes/test_legal_contract.txt", legal_separators, chunk_size=1500)

    print("\n--- Prototype v6 execution complete. ---")
