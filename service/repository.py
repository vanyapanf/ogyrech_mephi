from service.models import Project, Release, TestCase, TestPlan, TestRun, TestRunResult
from django.contrib.auth.models import User


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
            return TestPlan.objects.create(release=release)
        except Release.DoesNotExist:
            raise FileNotFoundError

    @staticmethod
    def find_release_by_id(release_id: int):
        try:
            return Release.objects.get(id=release_id)
        except Release.DoesNotExist:
            return None

    @staticmethod
    def find_test_runs_by_release_id(release):
        try:
            test_plan = TestPlan.objects.get(release=release)
            return TestRun.objects.filter(testPlan=test_plan)
        except TestPlan.DoesNotExist:
            raise FileNotFoundError

    @staticmethod
    def find_user_test_runs_by_release_id(user, release):
        try:
            test_plan = TestPlan.objects.get(release=release)
            return TestRun.objects.filter(testPlan=test_plan, user=user)
        except TestPlan.DoesNotExist:
            raise FileNotFoundError

    @staticmethod
    def find_user_by_user_name(user_name):
        try:
            return User.objects.get(username=user_name)
        except User.DoesNotExist:
            return None

    @staticmethod
    def create_test_run(test_plan, test_runner, creator):
        return TestRun.objects.create(testPlan=test_plan, creator=creator, user=test_runner)

    @staticmethod
    def create_test_run_result(test_plan, test_run):
        return TestRunResult.objects.create(testPlan=test_plan, testRun=test_run)

