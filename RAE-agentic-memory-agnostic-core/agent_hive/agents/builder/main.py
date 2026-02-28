"""
RAE Hive Builder (Autonomous Coder).
Executes coding tasks by using RAE as context and memory.
"""

import asyncio
import os
import re
import structlog
from base_agent.connector import HiveMindConnector

logger = structlog.get_logger(__name__)

async def builder_loop():
    connector = HiveMindConnector(agent_role="builder")
    logger.info("builder_started", status="online")
    
    await connector.log_activity("Builder ready to improve codebase.")

    while True:
        try:
            # 1. Fetch assigned tasks
            tasks = await connector.get_tasks(status="pending")

            for task in tasks:
                task_id = task["metadata"].get("task_id")
                objective = task["content"]
                logger.info("executing_coding_task", task_id=task_id, objective=objective)
                
                await connector.update_task(task["id"], status="in_progress")
                await connector.log_activity(f"Working on: {objective}")

                # 2. Use RAE to "think" about the implementation
                thought_prompt = f"""
                Objective: {objective}
                Instructions:
                1. Read the relevant files in /app/src.
                2. Plan the changes to improve determinism or performance.
                3. Provide the full code or patch.
                Format:
                Start your response with a line like: # /app/src/path/to/file.py
                Followed by the Python code in a block:
                ```python
                # code
                ```
                """
                
                plan = await connector.think(thought_prompt)
                
                # 3. Apply changes (Production Mode: Writing to /app/src)
                # Robust extraction: find path and code block anywhere in the plan
                path_match = re.search(r'# (/app/src/[^\s\n]+)', plan)
                code_match = re.search(r'```python\s*(.*?)\s*```', plan, re.DOTALL)
                
                if path_match and code_match:
                    target_path = path_match.group(1).replace("/app/src/", "").strip()
                    clean_code = code_match.group(1).strip()
                    
                    connector.write_source_file(target_path, clean_code)
                    logger.info("file_implemented", path=target_path)
                    await connector.update_task(task["id"], status="review", result=target_path)
                else:
                    logger.warning("pattern_match_failed_falling_back", task_id=task_id)
                    # Fallback to work_dir if pattern matching fails
                    result_filename = f"implementation_{task_id}.py"
                    with open(os.path.join("/app/work_dir", result_filename), "w") as f:
                        f.write(plan)
                    await connector.update_task(task["id"], status="review", result=result_filename)
                
                await connector.log_activity(f"Proposed implementation for {task_id} ready for audit.")

        except Exception as e:
            logger.error("builder_error", error=str(e))
            
        await asyncio.sleep(20)

if __name__ == "__main__":
    asyncio.run(builder_loop())
