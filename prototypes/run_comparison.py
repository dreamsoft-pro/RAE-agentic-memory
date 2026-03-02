"""
Comparison Benchmark v2: Old `IngestSegmenter` vs. New `SemanticRecursiveSegmenter`
Author: Gemini Agent (in research mode)
Date: 2026-02-18
Branch: research/segmenter-overhaul

Purpose: To directly compare the chunking output of the existing RAE segmenter
         (simplified to its default paragraph-splitting logic) against the new,
         research-backed prototype (v6).
"""
import numpy as np
import re
from typing import List, Optional, Dict, Any
import sys
sys.path.append('/app')

# --- Simplified Interfaces for self-containment ---
class IngestChunk:
    def __init__(self, content: str, metadata: dict = None, offset: int = 0, length: int = 0):
        self.content = content
        self.metadata = metadata or {}
        self.offset = offset
        self.length = length if length > 0 else len(content)
    def __repr__(self):
        return f"IngestChunk(len={self.length})"

# ---
# BEGIN: Clean, simplified implementation of the core logic of the "Old Method"
# ---
class Old_IngestSegmenter_Simplified:
    def __init__(self, target_size=1500):
        self.target_size = target_size

    def segment(self, text: str) -> List[IngestChunk]:
        """Simplified to only use the default paragraph-based splitting and aggregation."""
        # 1. Split into "atoms" (paragraphs)
        atoms = [p.strip() for p in text.split('\n\n') if p.strip()]
        if not atoms: 
            return [IngestChunk(text)] if text.strip() else []
        
        # 2. Aggregate atoms into chunks
        chunks = []
        current_group = []
        current_size = 0
        for atom in atoms:
            atom_size = len(atom)
            # If adding the next atom makes the chunk too big, finalize the current one
            if current_size + atom_size > self.target_size and current_group:
                chunks.append(IngestChunk("\n\n".join(current_group)))
                current_group, current_size = [atom], atom_size
            else:
                current_group.append(atom)
                current_size += atom_size + (2 if current_group else 0)
        
        if current_group:
            chunks.append(IngestChunk("\n\n".join(current_group)))
            
        return chunks
# ---
# END: Clean implementation of the "Old Method"
# ---


# ---
# BEGIN: Import the "New Method" from the v6 prototype
# ---
# This assumes the 'prototypes' directory is in the python path.
# Since we run from the root of the project, this should work.
from prototypes.segmenter_prototype import SemanticRecursiveSegmenter
# ---
# END: Import of the "New Method"
# ---


def print_comparison(file_path: str, old_chunks: list, new_chunks: list):
    """Prints a formatted comparison of the two segmentation methods."""
    print("\n" + "="*80)
    print(f"COMPARISON BENCHMARK: {file_path}")
    print("="*80)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text_len = len(f.read())
    except:
        text_len = -1
    
    print(f"\n--- Method 1: Old `IngestSegmenter` (Default Paragraph Split) ---")
    if old_chunks:
        old_lengths = [c.length for c in old_chunks]
        print(f"Result: {len(old_lengths)} chunks created from text of length {text_len}.")
        print(f"Stats: Avg len: {np.mean(old_lengths):.2f}, Std Dev: {np.std(old_lengths):.2f}, Min: {np.min(old_lengths)}, Max: {np.max(old_lengths)}")
    else:
        print("Result: No chunks created.")
    
    print(f"\n--- Method 2: New `SemanticRecursiveSegmenter` (Hybrid) ---")
    if new_chunks:
        new_lengths = [len(c) for c in new_chunks]
        print(f"Result: {len(new_lengths)} chunks created from text of length {text_len}.")
        print(f"Stats: Avg len: {np.mean(new_lengths):.2f}, Std Dev: {np.std(new_lengths):.2f}, Min: {np.min(new_lengths)}, Max: {np.max(new_lengths)}")
    else:
        print("Result: No chunks created.")
    
    print("\n--- Qualitative Sample (First 3 Chunks of Each Method) ---")
    print("\nOLD METHOD:")
    for i, chunk in enumerate(old_chunks[:3]):
        clean_content = chunk.content[:150].strip().replace("\n", " ")
        print(f"  Chunk {i+1} (len: {chunk.length}): '{clean_content}...'")
    
    print("\nNEW METHOD:")
    for i, chunk in enumerate(new_chunks[:3]):
        clean_content = chunk[:150].strip().replace("\n", " ")
        print(f"  Chunk {i+1} (len: {len(chunk)}): '{clean_content}...'")
    
    print("-" * 80)


if __name__ == "__main__":
    
    # --- Configuration ---
    TEST_FILES = {
        "legal": {
            "path": "/app/prototypes/test_legal_contract.txt",
            "old_chunk_size": 2000,
            "new_chunk_size": 2000,
            "new_separators": ["\n## ARTICLE ", "\n\n**", "\n\n", "\n"]
        },
        "scientific": {
            "path": "/app/prototypes/test_scientific_paper.md",
            "old_chunk_size": 1200,
            "new_chunk_size": 1200,
            "new_separators": ["\n## ", "\n### ", "\n\n---", "\n\n", "\n"]
        },
        "code": {
            "path": "/app/prototypes/test_complex_code.py",
            "old_chunk_size": 1500,
            "new_chunk_size": 1500,
            "new_separators": ["\n\n\n", "\nclass ", "\ndef ", "\n# ---", "\n\n"]
        }
    }
    
    # --- Execution ---
    for test_name, config in TEST_FILES.items():
        try:
            with open(config["path"], "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"\n[ERROR] Test file not found for '{test_name}': {config['path']}")
            continue
            
        # Run Old Method
        old_segmenter = Old_IngestSegmenter_Simplified(target_size=config["old_chunk_size"])
        old_chunks = old_segmenter.segment(text)
        
        # Run New Method
        new_segmenter = SemanticRecursiveSegmenter(
            structural_separators=config["new_separators"],
            chunk_size=config["new_chunk_size"]
        )
        new_chunks = new_segmenter.segment(text)
        
        print_comparison(config["path"], old_chunks, new_chunks)
