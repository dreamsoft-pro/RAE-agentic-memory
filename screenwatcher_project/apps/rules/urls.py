from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RuleViewSet, RuleSimulationView, RuleEditorView

router = DefaultRouter()
router.register(r'rules', RuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('simulate/', RuleSimulationView.as_view(), name='rule-simulate'),
    path('editor/', RuleEditorView.as_view(), name='rule-editor'),
]