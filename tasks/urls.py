from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"tasks", views.TaskViewSet, basename='task')

urlpatterns = [
  path("", include(router.urls)),
]