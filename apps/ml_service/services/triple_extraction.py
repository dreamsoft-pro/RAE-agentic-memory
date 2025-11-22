"""
Triple Extraction Service - Extract knowledge triples from text.

Extracts structured knowledge in the form of (subject, predicate, object) triples
using spaCy's dependency parsing.
"""

from typing import List, Dict, Any
import structlog

logger = structlog.get_logger(__name__)


class TripleExtractionService:
    """
    Service for extracting knowledge triples from natural language text.

    Uses dependency parsing to identify subject-verb-object relationships
    and converts them into structured triples.
    """

    _instance = None
    _nlp = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, language: str = "en"):
        """
        Initialize triple extraction service.

        Args:
            language: Language code (default: "en")
        """
        if self._nlp is None:
            try:
                import spacy
                logger.info("loading_spacy_for_triples", language=language)

                # Load spaCy model
                try:
                    if language == "en":
                        # Try models in order of preference
                        for model_name in ["en_core_web_lg", "en_core_web_md", "en_core_web_sm"]:
                            try:
                                self._nlp = spacy.load(model_name)
                                logger.info("spacy_loaded_for_triples", model=model_name)
                                break
                            except OSError:
                                continue
                    else:
                        self._nlp = spacy.load(f"{language}_core_news_sm")
                        logger.info("spacy_loaded_for_triples", model=f"{language}_core_news_sm")

                    if self._nlp is None:
                        # Fall back to blank model
                        self._nlp = spacy.blank(language)
                        logger.warning("using_blank_spacy_model", language=language)

                except Exception as e:
                    logger.error("spacy_loading_failed", error=str(e))
                    self._nlp = spacy.blank(language)

            except ImportError as e:
                logger.error("spacy_not_installed", error=str(e))
                raise RuntimeError("spaCy not installed")

    def extract_triples(self, text: str, language: str = "en") -> List[Dict[str, str]]:
        """
        Extract knowledge triples from text using dependency parsing.

        Args:
            text: Input text to process
            language: Language code

        Returns:
            List of triple dictionaries with subject, predicate, and object
        """
        if not text:
            return []

        logger.info("extracting_triples", text_length=len(text))

        try:
            doc = self._nlp(text)
            triples = []

            # Process each sentence
            for sent in doc.sents:
                # Find triples using dependency patterns
                sent_triples = self._extract_triples_from_sentence(sent)
                triples.extend(sent_triples)

            logger.info(
                "triples_extracted",
                triple_count=len(triples),
                text_length=len(text)
            )

            return triples

        except Exception as e:
            logger.exception("triple_extraction_failed", error=str(e))
            return []

    def _extract_triples_from_sentence(self, sent) -> List[Dict[str, str]]:
        """
        Extract triples from a single sentence using dependency parsing.

        Args:
            sent: spaCy Span object representing a sentence

        Returns:
            List of triples found in the sentence
        """
        triples = []

        # Find the main verb (ROOT of the sentence)
        for token in sent:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                # This is the main predicate
                predicate = token.lemma_

                # Find subject
                subject = self._find_subject(token)
                # Find object
                obj = self._find_object(token)

                if subject and obj:
                    triples.append({
                        "subject": subject,
                        "predicate": predicate,
                        "object": obj,
                        "confidence": 0.8  # Simple heuristic confidence
                    })

                # Handle conjunctions (e.g., "Bob loves Alice and Charlie")
                for conj in token.conjuncts:
                    if conj.pos_ == "VERB":
                        conj_obj = self._find_object(conj)
                        if subject and conj_obj:
                            triples.append({
                                "subject": subject,
                                "predicate": conj.lemma_,
                                "object": conj_obj,
                                "confidence": 0.7
                            })

        return triples

    def _find_subject(self, verb_token) -> str:
        """
        Find the subject of a verb.

        Args:
            verb_token: spaCy Token representing the verb

        Returns:
            String representation of the subject, or None
        """
        # Look for nominal subject (nsubj) or clausal subject (csubj)
        for child in verb_token.children:
            if child.dep_ in ["nsubj", "nsubjpass", "csubj"]:
                # Get the full noun phrase
                return self._get_full_phrase(child)

        return None

    def _find_object(self, verb_token) -> str:
        """
        Find the object of a verb.

        Args:
            verb_token: spaCy Token representing the verb

        Returns:
            String representation of the object, or None
        """
        # Look for direct object (dobj), indirect object (iobj), or prepositional object (pobj)
        for child in verb_token.children:
            if child.dep_ in ["dobj", "dative", "attr"]:
                return self._get_full_phrase(child)

            # Handle prepositional phrases
            if child.dep_ == "prep":
                for prep_child in child.children:
                    if prep_child.dep_ == "pobj":
                        return self._get_full_phrase(prep_child)

        return None

    def _get_full_phrase(self, token) -> str:
        """
        Get the full noun phrase for a token (including modifiers).

        Args:
            token: spaCy Token

        Returns:
            String representation of the full phrase
        """
        # Get all tokens in the subtree
        subtree = list(token.subtree)

        # Sort by position in sentence
        subtree.sort(key=lambda x: x.i)

        # Join tokens to form phrase
        phrase = " ".join([t.text for t in subtree])

        return phrase.strip()

    def extract_simple_triples(self, text: str) -> List[Dict[str, str]]:
        """
        Simplified triple extraction using basic patterns.

        This is a fallback method that uses simpler patterns and is faster
        but potentially less accurate than full dependency parsing.

        Args:
            text: Input text

        Returns:
            List of extracted triples
        """
        try:
            doc = self._nlp(text)
            triples = []

            # Simple pattern: find ENTITY1 - VERB - ENTITY2
            for sent in doc.sents:
                entities = [ent for ent in sent.ents]

                # If we have at least 2 entities and a verb
                if len(entities) >= 2:
                    # Find verbs in the sentence
                    verbs = [token for token in sent if token.pos_ == "VERB"]

                    if verbs:
                        # Create simple triples from entity pairs and verbs
                        for i, subj in enumerate(entities[:-1]):
                            for obj in entities[i+1:]:
                                for verb in verbs:
                                    # Only if verb is between the entities
                                    if subj.end <= verb.i <= obj.start:
                                        triples.append({
                                            "subject": subj.text,
                                            "predicate": verb.lemma_,
                                            "object": obj.text,
                                            "confidence": 0.6  # Lower confidence for simple method
                                        })

            return triples

        except Exception as e:
            logger.exception("simple_triple_extraction_failed", error=str(e))
            return []
