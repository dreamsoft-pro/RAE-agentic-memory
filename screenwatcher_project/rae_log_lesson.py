from rae_task_bridge import RAETaskBridge

def log_failure():
    bridge = RAETaskBridge()
    msg = "DELEGATION LESSON: Direct automated delegation to Node1 (kubus-gpu-01) via '/control/tasks' currently returns 'unknown_task_type' for all guessed types. RAE Execute Pipeline ('/v1/agent/execute') fails due to localhost Ollama connection. Node1 is ONLINE but protocol needs refinement. Proceeding with manual implementation of Phase 7 to avoid drift and save developer time."
    bridge.log_lesson("screenwatcher_project", msg)
    print("Lesson logged to RAE.")

if __name__ == "__main__":
    log_failure()
