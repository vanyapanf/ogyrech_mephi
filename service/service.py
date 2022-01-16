from service.repository import ProjectRepository as DB


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
