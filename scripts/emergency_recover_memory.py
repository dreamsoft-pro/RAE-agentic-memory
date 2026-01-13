import asyncio

import asyncpg


async def recover():
    print("🚀 Starting Cognitive Layer Restoration...")
    conn = await asyncpg.connect("postgresql://rae:rae_password@localhost:5432/rae")

    # 1. Normalizacja nazw warstw
    layer_map = {
        "em": "episodic",
        "ltm": "semantic",
        "sm": "semantic",
        "rm": "reflective",
        "stm": "working",
        "wm": "working",
    }

    for old, new in layer_map.items():
        count = await conn.execute(
            "UPDATE memories SET layer = $1 WHERE layer = $2", new, old
        )
        print(f"  - Normalized '{old}' -> '{new}': {count}")

    # 2. Przeniesienie surowych logów z semantic do episodic
    # Kryterium: content zawiera frazy logowe (ERROR, CRITICAL, log message, issue) lub source jest systemowy
    move_count = await conn.execute(
        """
        UPDATE memories 
        SET layer = 'episodic' 
        WHERE layer = 'semantic' 
        AND (
            content ~* 'log message|error:|critical:|priority:|status:|issue'
            OR source IN ('system', 'logger', 'monitoring')
        )
    """
    )
    print(f"  - Moved raw logs from 'semantic' to 'episodic': {move_count}")

    # 3. Naprawa brakujących agent_id (zabezpieczenie kontraktu)
    fix_agent = await conn.execute(
        "UPDATE memories SET agent_id = 'default' WHERE agent_id IS NULL OR agent_id = ''"
    )
    print(f"  - Fixed missing agent_ids: {fix_agent}")

    # 4. Sprawdzenie stanu po operacji
    print("\n--- Final Layer Distribution ---")
    rows = await conn.fetch(
        "SELECT layer, COUNT(*) FROM memories GROUP BY layer ORDER BY count DESC"
    )
    for r in rows:
        print(f"Warstwa: {str(r['layer']):<15} | Ilosc: {r['count']}")

    await conn.close()
    print("\n✅ Restoration Complete.")


if __name__ == "__main__":
    asyncio.run(recover())
