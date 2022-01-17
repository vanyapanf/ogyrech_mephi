from service.models import TestRun, TestPlan, TestRunResult


class TestRunWrapper:
    def __init__(self, test_run: TestRun, test_plan: TestPlan):
        try:
            self.id = test_run.id
            self.testRunner = test_run.user
            self.creator = test_run.creator
            result = test_run.testrunresult_set.get(testPlan=test_plan)
            self.num_of_test = result.testRun.testCase.all().count()
            self.successfull_test = result.successfulTestes
            self.failed_test = result.failedTestes
            self.not_run = self.num_of_test - self.successfull_test - self.failed_test
            if self.not_run < 0:
                raise ValueError
        except TestRunResult.DoesNotExist:
            raise FileNotFoundError

