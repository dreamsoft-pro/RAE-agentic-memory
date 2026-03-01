from django.db import models
from apps.core.models import BaseModel
from apps.core.fields import LegacyJSONField
from apps.registry.models import Machine

class Rule(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Optional: Link rule to specific machine. If null, rule is global (or filtered by tags in logic).
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True, related_name='rules')
    
    # The logic in json-logic format. Example: {"all": [{"var": "temp"}, {">": [{"var": "temp"}, 80]}]}
    logic = LegacyJSONField(default=dict, help_text="Rule logic in JsonLogic format")
    
    # Definition of actions to take if rule matches.
    # Example: [{"type": "alert", "message": "High Temp!"}]
    actions = LegacyJSONField(default=list, help_text="List of actions to execute on hit")

    def __str__(self):
        return self.name

class RuleHit(BaseModel):
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='hits')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='rule_hits')
    
    # Snapshot of data that triggered the rule
    payload = LegacyJSONField(default=dict)
    
    # Result of actions (optional, to log what happened)
    action_log = LegacyJSONField(default=list, blank=True)

    def __str__(self):
        return f"Hit: {self.rule.name} on {self.machine.code} at {self.created_at}"
