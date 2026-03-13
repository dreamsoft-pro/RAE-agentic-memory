# RAE - Advanced Ingestion Logic (Segmentation Test)
# This file contains a more complex set of interacting classes and functions
# to rigorously test content-aware segmentation.

import re
from typing import List, Dict, Any

# --- Base Classes and Interfaces ---

class BaseProcessor:
    """An abstract base class for processing data."""
    def process(self, data: Any) -> Any:
        raise NotImplementedError("Each processor must implement its own process method.")

class Auditable:
    """A mixin class to add audit capabilities."""
    def __init__(self):
        self._audit_log = []

    def log_action(self, action: str, details: Dict):
        self._audit_log.append({"action": action, "details": details})
        print(f"[AUDIT] - {action}: {details}")

    def get_audit_trail(self) -> List[Dict]:
        return self._audit_log

# --- Concrete Implementations ---

class TextProcessor(BaseProcessor, Auditable):
    """
    A processor for cleaning and normalizing textual data.
    A good segmenter should try to keep this entire class within one chunk.
    """
    def __init__(self, lowercase: bool = True, remove_punctuation: bool = False):
        super().__init__() # Initialize Auditable mixin
        self.lowercase = lowercase
        self.remove_punctuation = remove_punctuation
        self.log_action("init", {"class": "TextProcessor", "lowercase": lowercase})

    def process(self, text: str) -> str:
        self.log_action("process_start", {"input_length": len(text)})
        
        if self.lowercase:
            text = text.lower()
        
        if self.remove_punctuation:
            text = re.sub(r'[^\w\s]', '', text)
            
        self.log_action("process_end", {"output_length": len(text)})
        return text

class Vectorizer(BaseProcessor):
    """
    Responsible for converting text into vector embeddings.
    This class is another logical unit that should ideally not be split.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        # In a real scenario, the model would be loaded here.
        print(f"Vectorizer initialized with model: {self.model_name}")

    def process(self, text: str) -> List[float]:
        """Simulates converting text to a dense vector."""
        print(f"Vectorizing text of length {len(text)}...")
        # This is a mock implementation. A real implementation would use a
        # sentence-transformer or ONNX model to generate embeddings.
        # The length of the vector is determined by the text length for this mock.
        vector_length = len(text) % 1024
        return [float(i) for i in range(vector_length)]

# --- Standalone Utility Function ---

def run_processing_pipeline(text_data: str, config: Dict):
    """
    A standalone function that orchestrates the use of the processors.
    This function represents a complete, self-contained logical block.
    A perfect segmenter would place this entire function in a single chunk.
    """
    print("
--- Starting New Processing Pipeline ---")
    
    # 1. Initialize and run the text processor
    text_processor = TextProcessor(
        lowercase=config.get("use_lowercase", True),
        remove_punctuation=config.get("remove_punctuation", False)
    )
    cleaned_text = text_processor.process(text_data)
    
    # 2. Initialize and run the vectorizer
    vectorizer = Vectorizer(model_name=config.get("vector_model", "all-MiniLM-L6-v2"))
    vector = vectorizer.process(cleaned_text)
    
    # 3. Log the final output
    print(f"Successfully processed and vectorized text.")
    print(f"Final vector dimension: {len(vector)}")
    
    # 4. Return the full audit trail
    return text_processor.get_audit_trail()

# --- Main Execution Block for Demonstration ---
if __name__ == "__main__":
    
    sample_config = {
        "use_lowercase": True,
        "remove_punctuation": True,
        "vector_model": "bge-large-en-v1.5"
    }
    
    long_text_input = (
        "This is the INPUT document. It contains various punctuation marks like commas (,), periods (.), "
        "and exclamation marks! The GOAL is to process it through the pipeline. "
        "The pipeline should first clean the text according to the configuration, "
        "and then generate a vector representation of the cleaned content."
    )
    
    run_processing_pipeline(long_text_input, sample_config)

    # Second run with different config
    sample_config_2 = {"use_lowercase": False}
    run_processing_pipeline("Another Run with Different Settings.", sample_config_2)
