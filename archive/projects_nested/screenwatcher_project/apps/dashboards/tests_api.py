import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.dashboards.models import Dashboard, Widget
from apps.rbac.services import EnforcerService

@pytest.mark.django_db
class TestDashboardAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        
        # Initialize Casbin permissions for dashboard access
        EnforcerService.add_policy(self.user.username, 'dashboards.dashboard', 'read')
        EnforcerService.add_policy(self.user.username, 'dashboards.dashboard', 'write')
        EnforcerService.add_policy(self.user.username, 'dashboards.widget', 'read')
        EnforcerService.add_policy(self.user.username, 'dashboards.widget', 'write')
        EnforcerService.add_policy(self.user.username, 'dashboards.widget', 'update')
        EnforcerService.add_policy(self.user.username, 'dashboards.widget', 'delete')
        EnforcerService.get_enforcer().save_policy()

        self.dashboard = Dashboard.objects.create(user=self.user, name="My Dashboard")

    def test_list_dashboards(self):
        url = '/dashboard/api/management/'
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_create_widget(self):
        url = '/dashboard/api/widgets/'
        data = {
            "dashboard": self.dashboard.id,
            "title": "Temperature",
            "widget_type": "oee_gauge",
            "config": {"min": 0, "max": 100},
            "x": 0, "y": 0, "w": 4, "h": 4
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        assert Widget.objects.filter(dashboard=self.dashboard).count() == 1

    def test_update_widget_position(self):
        widget = Widget.objects.create(
            dashboard=self.dashboard, 
            title="Old", 
            widget_type="status_card",
            pos_x=0, pos_y=0, width=2, height=2
        )
        url = f'/dashboard/api/widgets/{widget.id}/'
        # Using aliased fields from serializer
        data = {"x": 5, "y": 10}
        
        response = self.client.patch(url, data, format='json')
        assert response.status_code == 200
        widget.refresh_from_db()
        assert widget.pos_x == 5
        assert widget.pos_y == 10

    def test_delete_widget(self):
        widget = Widget.objects.create(
            dashboard=self.dashboard, 
            title="To Delete", 
            widget_type="status_card",
            pos_x=0, pos_y=0, width=2, height=2
        )
        url = f'/dashboard/api/widgets/{widget.id}/'
        response = self.client.delete(url)
        assert response.status_code == 204
        assert not Widget.objects.filter(id=widget.id).exists()
