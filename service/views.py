import json
import jsonpickle
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from service.pages import ERROR, PROJECTS, ADD_PROJECT, RELEASES, TEST_CASES, TEST_RUNS, TEST_RUNS_TEST_CASES, \
    ADD_TEST_CASE, ADD_TEST_CASE_TO_TEST_RUN
from service.service import ProjectService


def body_to_dict(body: HttpRequest.body) -> dict or list:
    return json.loads(body)


def return_data(func):
    def wrapper(*args, **kwargs) -> HttpResponse:
        data = func(*args, **kwargs)
        data_json = jsonpickle.encode(data, unpicklable=False)
        return HttpResponse(data_json, content_type='application/json')

    return wrapper


def return_data_template(func):
    def wrapper(*args, **kwargs) -> HttpResponse:
        request, data = func(*args, **kwargs)
        if not data['ok']:
            return render(request, ERROR.get_html(), context=data)
        return render(request, f'{data["template"]}.html', data)

    return wrapper


def redirect_dec(function, page_to):
    def _function(request, *args, **kwargs):
        function(request, *args, **kwargs)
        return redirect(page_to)
    return _function


@csrf_exempt
@login_required(login_url='login')
@permission_required('add_project', login_url='login')
@return_data_template
def create_project(request: HttpRequest):
    if request.method == 'POST':
        try:
            print()
            body = body_to_dict(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return request, {'ok': False, 'error': 'InvalidBody'}
        try:
            ProjectService.create_project(**body)
            projects = ProjectService.find_projects()
        except ValueError:
            data = {'error': 'ValueError', 'ok': False, 'message': 'InvalidBody'}
        except FileExistsError:
            data = {'error': 'FileExistsError', 'ok': False, 'message': 'Project already exist'}
        else:
            data = {'ok': True,
                    'projects': projects,
                    'template': PROJECTS.get_full_name(),
                    'action': 'FIND',
                    'body': 'projects'
                    }
        return request, data
    elif request.method == 'GET':
        return request, {'ok': True, 'template': ADD_PROJECT.get_full_name()}
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@login_required(login_url='login')
@return_data_template
def find_projects(request):
    projects = ProjectService.find_projects()
    data = {'ok': True, 'projects': projects, 'template': PROJECTS.get_full_name(), 'action': 'FIND',
            'body': 'projects'}
    return request, data


@login_required(login_url='login')
@permission_required('view_release', login_url='login')
@return_data_template
def open_project_releases(request, project_id: int):
    if request.method == 'GET':
        project, releases = ProjectService.get_releases_by_project_id(project_id)
        data = {'ok': True,
                'project': project,
                'releases': releases,
                'template': RELEASES.get_full_name()
                }
        return request, data
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@csrf_exempt
@login_required(login_url='login')
@permission_required('add_release', login_url='login')
@return_data_template
def create_release(request: HttpRequest):
    if request.method == 'POST':
        try:
            body = body_to_dict(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return request, {'ok': False, 'error': 'InvalidBody'}
        try:
            release = ProjectService.create_release(**body)
            project, releases = ProjectService.get_releases_by_project_id(release.project_id)
        except ValueError or TypeError:
            data = {'error': 'ValueError', 'ok': False, 'message': 'InvalidBody'}
        except FileExistsError:
            data = {'error': 'FileExistsError', 'ok': False, 'message': 'Project already exist'}
        else:
            data = {'ok': True,
                    'project': project,
                    'releases': releases,
                    'template': RELEASES.get_full_name()
                    }
        return request, data
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@login_required(login_url='login')
@permission_required('view_testcase', login_url='login')
@return_data_template
def find_test_cases(request):
    test_cases = ProjectService.find_test_cases()
    data = {'ok': True, 'test_cases': test_cases, 'template': TEST_CASES.get_full_name(), 'action': 'FIND',
            'body': 'projects'}
    return request, data


@csrf_exempt
@login_required(login_url='login')
@permission_required('add_testcase', login_url='login')
@return_data_template
def create_test_case(request: HttpRequest):
    if request.method == 'POST':
        try:
            body = body_to_dict(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return request, {'ok': False, 'error': 'InvalidBody'}
        try:
            ProjectService.create_test_case(**body)
            test_cases = ProjectService.find_test_cases()
        except ValueError or TypeError:
            data = {'error': 'ValueError', 'ok': False, 'message': 'InvalidBody'}
        except FileExistsError:
            data = {'error': 'FileExistsError', 'ok': False, 'message': 'Test case already exist'}
        else:
            data = {'ok': True,
                    'test_cases': test_cases,
                    'template': TEST_CASES.get_full_name(),
                    'action': 'FIND',
                    'body': 'test_cases'}
        return request, data
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@login_required(login_url='login')
@permission_required('view_testrun', login_url='login')
@return_data_template
def open_release_test_runs(request, project_id: int, release_id: int):
    if request.method == 'GET':
        user = request.user
        if user.groups.filter(name='Администратор').exists() or user.is_superuser:
            release, test_runs = ProjectService.get_test_runs_by_release_id(release_id)

        else:
            release, test_runs = ProjectService.get_user_test_runs_by_release_id(user, release_id)

        data = {'ok': True,
                'test_runs': test_runs,
                'release': release,
                'template': TEST_RUNS.get_full_name()
                }
        return request, data
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@csrf_exempt
@login_required(login_url='login')
@permission_required('add_testrun', login_url='login')
@return_data_template
def create_test_run(request, project_id: int, release_id: int):
    if request.method == 'POST':
        try:
            body = body_to_dict(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return request, {'ok': False, 'error': 'InvalidBody'}
        try:
            ProjectService.create_test_run(request.user, **body)
            user = request.user
            if user.groups.filter(name='Администратор').exists() or user.is_superuser:
                release, test_runs = ProjectService.get_test_runs_by_release_id(release_id)
            else:
                release, test_runs = ProjectService.get_user_test_runs_by_release_id(user, release_id)
            data = {'ok': True,
                    'test_runs': test_runs,
                    'release': release,
                    'template': TEST_RUNS.get_full_name()
                    }
            return request, data
        except ValueError or TypeError:
            data = {'error': 'ValueError', 'ok': False, 'message': 'InvalidBody'}
            return request, data
        except FileExistsError:
            data = {'error': 'FileExistsError', 'ok': False, 'message': 'Project already exist'}
            return request, data
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@login_required(login_url='login')
@permission_required('view_testrun', login_url='login')
@return_data_template
def open_test_run(request, release_id: int, testrun_id: int):
    if request.method == 'GET':
        user = request.user
        test_run = ProjectService.get_test_run_by_id(testrun_id)
        if not user.groups.filter(name='Администратор').exists() and not user.is_superuser:
            if test_run.user != user:
                data = {'error': 'PermissionError', 'ok': False, 'message': 'Нет прав доступа к станица'}
                return request, data
        data = {'ok': True,
                'release_id': release_id,
                'test_run': test_run,
                'test_cases': list(test_run.testCase.all()),
                'template': TEST_RUNS_TEST_CASES.get_full_name()
                }
        return request, data
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@csrf_exempt
@login_required(login_url='login')
@permission_required('add_testcaseresult', login_url='login')
#@return_data_template
def add_test_case_to_test_run(request, release_id: int, testrun_id: int):
    if request.method == 'POST':
        try:
            body = body_to_dict(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return request, {'ok': False, 'error': 'InvalidBody'}
        try:

            ProjectService.add_test_cases_to_test_run(testrun_id, **body)
            return redirect('open_test_run', release_id=release_id,testrun_id=testrun_id)
        except ValueError or TypeError:
            data = {'error': 'ValueError', 'ok': False, 'message': 'InvalidBody'}
        except FileExistsError:
            data = {'error': 'FileExistsError', 'ok': False, 'message': 'Project already exist'}
        return render(request, ERROR.get_html(), context=data)
    else:
        return render(request, ERROR.get_html(), context={'ok': False, 'error': 'InvalidMethod'})


@login_required(login_url='login')
@permission_required('add_testcaseresult', login_url='login')
@return_data_template
def get_test_run_test_cases(request, release_id: int, testrun_id: int):
    if request.method == 'GET':
        test_cases = ProjectService.find_test_cases_not_included_in_test_run(testrun_id=testrun_id)
        data = {'ok': True,
                'release_id': release_id,
                'testrun_id': testrun_id,
                'test_cases': test_cases,
                'template': f'{ADD_TEST_CASE_TO_TEST_RUN.get_full_name()}'
                }
        return request, data
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@csrf_exempt
@login_required(login_url='login')
@permission_required('add_testcaseresult', login_url='login')
# @return_data_template
def finish_test_case(request, release_id: int, testrun_id: int):
    if request.method == 'POST':
        try:
            body = body_to_dict(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return request, {'ok': False, 'error': 'InvalidBody'}
        try:
            ProjectService.finish_test_case(request.user, release_id, testrun_id, **body)
            return redirect('open_test_run', release_id=release_id, testrun_id=testrun_id)
        except ValueError or TypeError:
            data = {'error': 'ValueError', 'ok': False, 'message': 'InvalidBody'}
            return request, data
        except FileExistsError:
            data = {'error': 'FileExistsError', 'ok': False, 'message': 'Project already exist'}
            return render(request, ERROR.get_html(), context=data)
    else:
        return render(request, ERROR.get_html(), context={'ok': False, 'error': 'InvalidMethod'})