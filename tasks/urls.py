from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
  path("", views.TaskList.as_view(), name="index"),
  path("<int:pk>/", views.TaskDetail.as_view(), name="detail"),
  path("<int:pk>/highlight/", views.TaskHighlight.as_view(), name="highlight"),
]

urlpatterns = format_suffix_patterns(urlpatterns)