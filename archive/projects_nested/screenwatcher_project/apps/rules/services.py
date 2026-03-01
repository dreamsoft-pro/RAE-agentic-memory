from json_logic import jsonLogic
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)

class RuleEvaluator:
    @staticmethod
    def evaluate(logic, data):
        """
        Evaluate json-logic against data.
        Returns True if rule matches, False otherwise.
        """
        try:
            # jsonLogic returns the result of the logic.
            # In our case, we expect boolean logic for rules (matched or not).
            result = jsonLogic(logic, data)
            return bool(result)
        except Exception as e:
            logger.error(f"Error evaluating rule logic: {e}")
            return False

    @staticmethod
    def process_telemetry(telemetry_point):
        """
        Check all active rules against a telemetry point.
        Returns a list of created RuleHit objects.
        """
        from .models import Rule, RuleHit
        from .actions import ActionRegistry
        
        # 1. Fetch relevant rules
        # (Global rules OR rules assigned to this machine)
        rules = Rule.objects.filter(
            is_active=True
        ).filter(
            Q(machine__isnull=True) | Q(machine=telemetry_point.machine)
        )
        
        hits = []
        data = telemetry_point.payload
        # Add context (e.g. machine code) to data if needed by logic
        eval_context = data.copy()
        eval_context['machine_code'] = telemetry_point.machine.code
        eval_context['timestamp'] = str(telemetry_point.timestamp)
        
        for rule in rules:
            if RuleEvaluator.evaluate(rule.logic, eval_context):
                # HIT!
                
                # Execute Actions
                action_results = []
                for action_def in rule.actions:
                    ActionRegistry.execute(action_def, eval_context)
                    action_results.append({"type": action_def.get("type"), "status": "executed"})

                hit = RuleHit.objects.create(
                    rule=rule,
                    machine=telemetry_point.machine,
                    payload=data,
                    action_log=action_results
                )
                hits.append(hit)
                
        return hits
