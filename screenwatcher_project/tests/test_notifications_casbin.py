import pytest
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
from apps.rbac.services import EnforcerService
from apps.dashboards.models import Dashboard
from apps.rules.actions import ActionRegistry

User = get_user_model()

@pytest.mark.django_db
def test_notification_creation():
    user = User.objects.create_user(username="testuser", password="password")
    notification = Notification.objects.create(
        user=user,
        title="Test Alert",
        message="Machine over temperature",
        level="WARNING"
    )
    assert Notification.objects.filter(user=user).count() == 1
    assert notification.level == "WARNING"

@pytest.mark.django_db
def test_rule_action_notification():
    user = User.objects.create_user(username="ruleuser", password="password")
    context = {"machine_code": "M001"}
    params = {
        "level": "CRITICAL",
        "title": "Alert for {machine_code}",
        "message": "Critical failure detected",
        "user_ids": [user.id]
    }
    
    ActionRegistry.execute({"type": "notification", **params}, context)
    
    notification = Notification.objects.get(user=user)
    assert notification.title == "Alert for M001"
    assert notification.level == "CRITICAL"

@pytest.mark.django_db
def test_casbin_get_allowed_objects():
    # Note: This depends on the Casbin adapter being correctly configured with the test database
    EnforcerService.add_policy("admin", "dashboard_1", "read")
    EnforcerService.add_policy("admin", "dashboard_2", "read")
    
    allowed = EnforcerService.get_allowed_objects("admin", "read")
    assert "dashboard_1" in allowed
    assert "dashboard_2" in allowed
