from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OperatorViewSet, ReasonCodeViewSet, DowntimeSubmissionAPI, OperatorPanelView

router = DefaultRouter()
router.register(r'operators', OperatorViewSet)
router.register(r'reason-codes', ReasonCodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('declare/', DowntimeSubmissionAPI.as_view(), name='declare_downtime'),
    path('gui/', OperatorPanelView.as_view(), name='operator_gui'),
]
