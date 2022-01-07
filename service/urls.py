from django.urls import path, include
from . import views
from django.views.generic import TemplateView

from .pages import ADD_PROJECT, PROJECTS

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # all in service must be authenticated
    path(PROJECTS.name, views.find_projects),
    path(ADD_PROJECT.name, views.create_project),
]
