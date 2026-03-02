# RAE Core - Simplified Example for Segmentation Testing

class DataProcessor:
    """
    A simple class to demonstrate code segmentation.
    It contains a few methods with varying complexity.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key
        self.processed_items = 0

    def process_batch(self, items: list) -> int:
        """
        Processes a batch of items. A good chunk should contain this whole method.
        It iterates through items and calls a helper method.
        """
        if not items:
            return 0
        
        for item in items:
            self._process_single_item(item)
            
        return len(items)

    def _process_single_item(self, item: dict):
        """
        A private helper method to process a single item.
        This method is simple enough to be grouped with other methods.
        """
        # In a real scenario, this would involve more complex logic,
        # like calling an external API or performing a database lookup.
        item_id = item.get("id")
        if item_id:
            print(f"Processing item {item_id}...")
            self.processed_items += 1

def get_system_status() -> str:
    """
    A standalone function to get the system status.
    This function is independent of any class. A good segmenter
    might keep this function in a single chunk, potentially along
    with the DataProcessor class if space allows, or in a separate one
    if the class chunk is already full.
    """
    # This is a mock status check.
    # In a real system, this would check database connections,
    # API health, and other critical components.
    return "OK: All systems are operational."

# --- Main execution block ---
if __name__ == "__main__":
    print("RAE Segmentation Test Script")
    
    # Initialize the processor
    processor = DataProcessor(api_key="test-key-123")
    
    # Prepare some sample data
    sample_batch = [
        {"id": 1, "data": "alpha"},
        {"id": 2, "data": "beta"},
        {"id": 3, "data": "gamma"},
    ]
    
    # Process the data and print the results
    processed_count = processor.process_batch(sample_batch)
    print(f"Processed {processed_count} items.")
    
    # Check the system status
    status = get_system_status()
    print(f"System status: {status}")
