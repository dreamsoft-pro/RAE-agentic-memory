"""
Tests for Universal Ingest Pipeline (UICTC).
"""

import asyncio

from rae_core.ingestion.pipeline import UniversalIngestPipeline


async def test_procedural_ingest():
    pipeline = UniversalIngestPipeline()
    text = """
    Krok 1: Otwórz aplikację OneNote.
    Krok 2: Znajdź sekcję Order Entry.
    Uwaga: Pamiętaj o sprawdzeniu numeru zamówienia.
    Krok 3: Wpisz dane do systemu MES.
    """

    chunks, signature, audit, policy = await pipeline.process(text)

    assert signature.struct["mode"] == "LIST_PROCEDURE_LIKE"
    assert len(chunks) > 0
    assert chunks[0].metadata["ingest_policy"] == "POLICY_PROCEDURE_DOC"
    assert policy == "POLICY_PROCEDURE_DOC"
    print("✅ Procedural ingest test passed")

async def test_log_ingest():
    pipeline = UniversalIngestPipeline()
    text = "\n".join([
        f"2026-02-12 15:00:0{i} [INFO] Machine state: READY" for i in range(9)
    ])
    text += "\n2026-02-12 15:00:10 [INFO] Machine state: READY"

    # Needs more lines to trigger log mode in current simplistic detector
    long_log = (text + "\n") * 5

    chunks, signature, audit, policy = await pipeline.process(long_log)

    assert signature.struct["mode"] == "LINEAR_LOG_LIKE"
    assert chunks[0].metadata["ingest_policy"] == "POLICY_LOG_STREAM"
    assert policy == "POLICY_LOG_STREAM"
    print("✅ Log ingest test passed")

async def test_prose_ingest():
    pipeline = UniversalIngestPipeline()
    text = """
    RAE (Reflective Agentic-memory Engine) to zaawansowany system pamięci dla agentów AI.
    Zapewnia on deterministyczne i audytowalne zarządzanie wiedzą w środowiskach przemysłowych.
    System ten opiera się na matematycznych fundamentach i teorii grafów.
    """

    chunks, signature, audit, policy = await pipeline.process(text)

    assert signature.struct["mode"] == "PROSE_PARAGRAPH_LIKE"
    assert chunks[0].metadata["ingest_policy"] == "POLICY_PROSE_TEXT"
    assert policy == "POLICY_PROSE_TEXT"
    print("✅ Prose ingest test passed")

async def test_fallback_detection():
    pipeline = UniversalIngestPipeline()
    text = "STABILITY MODE ACTIVE (Math Fallback). Based on my memory manifold, here are the core facts: ..."

    chunks, signature, audit, policy = await pipeline.process(text)

    assert signature.struct["mode"] == "OPERATIONAL_FALLBACK"
    assert policy == "POLICY_FALLBACK"
    print("✅ Fallback detection test passed")

async def main():
    print("🚀 Starting Universal Ingest Tests...")
    await test_procedural_ingest()
    await test_log_ingest()
    await test_prose_ingest()
    await test_fallback_detection()
    print("🎉 All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())
