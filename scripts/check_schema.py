import asyncio
import os
import sys

import asyncpg

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.memory_api.config import settings


async def main():
    try:
        conn = await asyncpg.connect(
            host=settings.POSTGRES_HOST,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
        )

        # Check column type and precision
        query = """
            SELECT 
                column_name, 
                udt_name,
                character_maximum_length,
                numeric_precision
            FROM information_schema.columns 
            WHERE table_name = 'memory_embeddings' AND column_name = 'embedding'
        """
        row = await conn.fetchrow(query)
        print(f"Column: {row['column_name']}")
        print(f"Type: {row['udt_name']}")

        # For 'vector' type, dimension is in pg_attribute.atttypmod
        dim_query = "SELECT atttypmod FROM pg_attribute WHERE attrelid = 'memory_embeddings'::regclass AND attname = 'embedding'"
        atttypmod = await conn.fetchval(dim_query)
        print(f"atttypmod: {atttypmod} (if -1, dimension is flexible)")

        await conn.close()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
