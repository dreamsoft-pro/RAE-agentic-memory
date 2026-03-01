import logging
from typing import Callable, Dict, Any

logger = logging.getLogger(__name__)

class ActionRegistry:
    _actions: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(func: Callable):
            cls._actions[name] = func
            return func
        return decorator

    @classmethod
    def execute(cls, action_def: Dict[str, Any], context: Dict[str, Any]):
        """
        Executes an action based on definition.
        action_def example: {"type": "log", "level": "error", "message": "High temp!"}
        """
        action_type = action_def.get('type')
        if not action_type:
            logger.warning("Action definition missing 'type' field")
            return

        handler = cls._actions.get(action_type)
        if not handler:
            logger.warning(f"No handler registered for action type: {action_type}")
            return

        try:
            handler(action_def, context)
        except Exception as e:
            logger.error(f"Error executing action {action_type}: {e}")

# --- Standard Actions ---

@ActionRegistry.register("log")
def action_log(params: Dict[str, Any], context: Dict[str, Any]):
    level = params.get("level", "info").lower()
    msg = params.get("message", "Rule triggered")
    
    # Enrich message with context if needed using simple format
    # e.g. "Machine {machine_code} failure"
    try:
        msg = msg.format(**context)
    except KeyError:
        pass # Ignore formatting errors
        
    if level == "error":
        logger.error(f"[RULE ACTION] {msg}")
    elif level == "warning":
        logger.warning(f"[RULE ACTION] {msg}")
    else:
        logger.info(f"[RULE ACTION] {msg}")

@ActionRegistry.register("system_print")
def action_print(params: Dict[str, Any], context: Dict[str, Any]):
    """Useful for local debugging (visible in console stdout)"""
    msg = params.get("message", "")
    print(f"!!! SYSTEM ALERT !!! : {msg} | Context: {context.get('machine_code', '?')}")

@ActionRegistry.register("notification")
def action_notification(params: Dict[str, Any], context: Dict[str, Any]):
    """
    Creates a Notification for specified users.
    params: {"level": "INFO", "title": "...", "message": "...", "user_ids": [1, 2]}
    """
    from apps.notifications.models import Notification
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    level = params.get("level", "INFO")
    title = params.get("title", "Rule Alert")
    message = params.get("message", "A rule was triggered")
    user_ids = params.get("user_ids", [])

    # Format message with context
    try:
        title = title.format(**context)
        message = message.format(**context)
    except Exception:
        pass

    target_users = []
    if user_ids:
        target_users = User.objects.filter(id__in=user_ids)
    else:
        # Fallback: All active staff? Or admins?
        target_users = User.objects.filter(is_staff=True)

    for user in target_users:
        Notification.objects.create(
            user=user,
            level=level,
            title=title,
            message=message
        )
