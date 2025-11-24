from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Initialize the engines once and reuse them.
# This is a heavy object to create.
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


def scrub_text(text: str) -> str:
    """
    Analyzes and anonymizes PII in the given text using Presidio.
    """
    if not text:
        return ""

    # Analyze the text for PII entities
    analyzer_results = analyzer.analyze(text=text, language="en")

    # Anonymize the detected entities
    anonymized_text = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators={"DEFAULT": OperatorConfig("replace", {"new_value": "<PII>"})},
    )

    return anonymized_text.text
