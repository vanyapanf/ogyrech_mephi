from service.models import TestRun, TestPlan, TestRunResult


class TestRunWrapper:
    def __init__(self, test_run: TestRun, test_plan: TestPlan):
        try:
            id = test_run.id
            testRunner = test_run.user
            result = test_run.testrunresult_set.get(testPlan=test_plan)
            num_of_test = result.testRun.testCase.all().count()
            successfull_test_num = result.successfulTestes
            failed_test_num = result.failedTestes
            not_run = num_of_test - successfull_test_num - failed_test_num
            if not_run < 0:
                raise ValueError
        except TestRunResult.DoesNotExist:
            raise FileNotFoundError
