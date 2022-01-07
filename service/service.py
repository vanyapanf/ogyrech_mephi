from service.repository import ProjectRepository as DB


class ProjectService:
    @staticmethod
    def find_projects():
        return list(DB.find_projects().values())

    @staticmethod
    def create_project(**kwargs):
        name = kwargs.get('name')
        if name is None:
            raise ValueError
        return DB.create_project(name=name)
