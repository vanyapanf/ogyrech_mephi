from service.repository import ProjectRepository as DB
from service.wrappers import TestRunWrapper


class ProjectService:
    @staticmethod
    def find_projects():
        return list(DB.find_projects().values())

    @staticmethod
    def create_project(**kwargs):
        name = kwargs.get('name')
        description = kwargs.get('description')
        if name is None:
            raise ValueError
        return DB.create_project(name=name, description=description)

    @staticmethod
    def get_releases_by_project_id(project_id: int):
        if isinstance(project_id, int):
            project = DB.find_project_by_id(project_id)
            if project is not None:
                return project, DB.find_releases_by_project_id(project_id)
            else:
                raise FileNotFoundError
        else:
            raise TypeError

    @staticmethod
    def create_release(**kwargs):
        project_id = int(kwargs.get('project_id'))
        name = kwargs.get('name')
        description = kwargs.get('description')
        if project_id is None:
            raise ValueError
        if isinstance(project_id, int):
            project = DB.find_project_by_id(project_id=project_id)
            if project is not None:
                release = DB.create_release(project=project, name=name, description=description)
                DB.create_test_plan(release=release)
                return release
            else:
                raise FileNotFoundError
        else:
            raise TypeError

    @staticmethod
    def find_test_cases():
        return list(DB.find_test_cases().values())

    @staticmethod
    def create_test_case(**kwargs):
        expected_result = kwargs.get('expected_result')
        description = kwargs.get('description')
        if expected_result is None or description is None:
            raise ValueError
        return DB.create_test_case(description=description, expected_result=expected_result)

    @staticmethod
    def get_test_runs_by_release_id(release_id: int):
        release = DB.find_release_by_id(release_id=release_id)
        if release is not None:
            test_runs = DB.find_test_runs_by_release_id(release=release)
            result_test_runs = []
            for test_run in test_runs:
                result_test_runs.append(TestRunWrapper(test_run, release.testplan))

            return release, result_test_runs
        else:
            raise FileNotFoundError

    @staticmethod
    def get_user_test_runs_by_release_id(user, release_id):
        release = DB.find_release_by_id(release_id=release_id)
        if release is not None:
            return release, DB.find_user_test_runs_by_release_id(user=user,release=release)
        else:
            raise FileNotFoundError

    @staticmethod
    def create_test_run(creator, **kwargs):
        test_runner_user_name = kwargs.get('test_runner')
        release_id = int(kwargs.get('release_id'))

        if test_runner_user_name is None or release_id is None:
            raise ValueError
        test_runner = DB.find_user_by_user_name(test_runner_user_name)
        release = DB.find_release_by_id(release_id=release_id)
        if test_runner is not None:
            test_run = DB.create_test_run(release.testplan, test_runner, creator)
            DB.create_test_run_result(test_plan=release.testplan, test_run=test_run)
        else:
            raise FileNotFoundError
