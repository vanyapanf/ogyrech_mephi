from django.urls import path, include
from . import views
from django.views.generic import TemplateView

from .pages import ADD_PROJECT, PROJECTS, ADD_RELEASE, TEST_CASES, ADD_TEST_CASE, ADD_TEST_RUN, RELEASES

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # all in service must be authenticated
    path(PROJECTS.name, views.find_projects),
    path(ADD_PROJECT.name, views.create_project),
    path(f'{PROJECTS.name}/<int:project_id>', views.open_project_releases),
    path(f'{PROJECTS.name}/{ADD_RELEASE.name}', views.create_release),
    path(TEST_CASES.name, views.find_test_cases),
    path(ADD_TEST_CASE.name, views.create_test_case),
    path(f'{PROJECTS.name}/<int:project_id>/<int:release_id>', views.open_release_test_runs),
    path(f'{PROJECTS.name}/<int:project_id>/<int:release_id>/{ADD_TEST_RUN.name}', views.create_test_run),
    path(f'{RELEASES.name}/<int:release_id>/<int:testrun_id>',
         views.open_test_run,
         name='open_test_run'),
    path(f'{RELEASES.name}/<int:release_id>/<int:testrun_id>/{ADD_TEST_CASE.name}',
         views.add_test_case_to_test_run,
         name='add_test_case_to_test_run'),
    path(f'{RELEASES.name}/<int:release_id>/<int:testrun_id>/{TEST_CASES.name}',
         views.get_test_run_test_cases,
         name='get_test_run_test_cases')
]
