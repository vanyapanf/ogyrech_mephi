from service.models import Project


class ProjectRepository:
    @staticmethod
    def find_projects():
        return Project.objects.all()

    @staticmethod
    def create_project(name: str):
        try:
            Project.objects.get(name=name)
            raise FileExistsError
        except Project.DoesNotExist:
            project = Project.objects.create(name=name)
        return project.id
