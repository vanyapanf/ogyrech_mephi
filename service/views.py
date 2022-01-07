import json
import jsonpickle
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from service.pages import ERROR, PROJECTS, ADD_PROJECT
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


@csrf_exempt
@return_data_template
def create_project(request: HttpRequest):
    if request.method == 'POST':
        try:
            print()
            body = body_to_dict(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return request, {'ok': False, 'error': 'InvalidBody'}
        try:
            project_id = ProjectService.create_project(**body)
        except ValueError:
            data = {'error': 'ValueError', 'ok': False, 'message': 'InvalidBody'}
        except FileExistsError:
            data = {'error': 'FileExistsError', 'ok': False, 'message': 'Project already exist'}
        else:
            data = {'ok': True, 'id': project_id, 'template': PROJECTS.get_full_name(), 'action': 'Created',
                    'body': 'projects'}
        return request, data
    elif request.method == 'GET':
        return request, {'ok': True, 'template': ADD_PROJECT.get_full_name()}
    else:
        return request, {'ok': False, 'error': 'InvalidMethod'}


@return_data_template
def find_projects(request):
    projects = ProjectService.find_projects()
    data = {'ok': True, 'projects': projects, 'template': PROJECTS.get_full_name(), 'action': 'FIND',
            'body': 'projects'}
    return request, data
