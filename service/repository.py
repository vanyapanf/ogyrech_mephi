from datetime import time, datetime

from service.models import Project, Release, TestCase, TestPlan, TestRun, TestRunResult, TestCaseResult
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

    @staticmethod
    def create_test_case_result(test_case: TestCase, test_run: TestRun, test_run_result: TestRunResult, real_result, status):
        TestCaseResult.objects.create(
            testCase=test_case,
            testRun=test_run,
            testRunResult=test_run_result,
            isSuccessful=status,
            realResult=real_result,
            runDate=datetime.now()
        )

    @staticmethod
    def find_test_run_by_id(testrun_id):
        try:
            return TestRun.objects.get(id=testrun_id)
        except TestRun.DoesNotExist:
            raise FileNotFoundError

    @staticmethod
    def add_test_cases_to_test_run(testrun, case):
        testrun.testCase.add(case)

    @staticmethod
    def find_test_case_by_id(case_id: int):
        return TestCase.objects.get(id=case_id)

    @staticmethod
    def find_test_case_results(test_run, test_run_result):
        return TestCaseResult.objects.filter(testRun=test_run, testRunResult=test_run_result)

    @staticmethod
    def find_test_case_result(test_case_results, case: TestCase):
        try:
            return test_case_results.get(testCase=case)
        except TestCaseResult.DoesNotExist:
            return None
