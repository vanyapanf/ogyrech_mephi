from service.models import Project, Release, TestCase, TestPlan


class ProjectRepository:
    @staticmethod
    def find_projects():
        return Project.objects.all()

    @staticmethod
    def create_project(name: str, description: str):
        try:
            Project.objects.get(name=name)
            raise FileExistsError
        except Project.DoesNotExist:
            project = Project.objects.create(name=name, description=description)
        return project.id

    @staticmethod
    def find_project_by_id(project_id: int):
        try:
            return Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return None

    @staticmethod
    def find_releases_by_project_id(project_id: int):
        return Release.objects.filter(project_id=project_id)

    @staticmethod
    def create_release(project: Project, name: str, description: str):
        try:
            Release.objects.get(name=name)
            raise FileExistsError
        except Release.DoesNotExist:
            return Release.objects.create(project=project, name=name, description=description)

    @staticmethod
    def find_test_cases():
        return TestCase.objects.all()

    @staticmethod
    def create_test_case(description, expected_result):
        return TestCase.objects.create(description=description, expectedResult=expected_result)

    @staticmethod
    def create_test_plan(release):
        try:
            Release.objects.get(name=release.name)
            raise FileExistsError
        except Release.DoesNotExist:
            return TestPlan.objects.create(release=release)
