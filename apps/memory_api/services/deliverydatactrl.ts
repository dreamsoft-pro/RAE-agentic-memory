javascript
import '@/lib/api'; // Import the API module as per rule 3

// Assuming this is inside some async function or promise chain
async function processData(data) {
    try {
        const processedData = await processDataBackend(data); // [BACKEND_ADVICE]
        return processedData;
    } catch (error) {
        console.error('Error processing data:', error);
        throw new Error(`Failed to process data: ${error.message}`);
    }
}

// Backend logic for processing data
async function processDataBackend(data) {
    const result = await someHeavyApiCall(); // [BACKEND_ADVICE]
    return result;
}
