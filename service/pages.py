class Page:
    def __init__(self, name):
        self.name = name

    def get_html(self):
        return f'service/{self.name}.html'

    def get_full_name(self):
        return f'service/{self.name}'


INDEX = Page('index')
ERROR = Page('error')
ADD_USER = Page('add_user')
PROJECTS = Page('projects')
ADD_PROJECT = Page(name='add_project')
RELEASES = Page('releases')
ADD_RELEASE = Page('add_release')
TEST_CASES = Page('test_cases')
ADD_TEST_CASE = Page('add_test_case')
TEST_RUNS = Page('test_runs')
ADD_TEST_RUN = Page('add_testrun')
TEST_RUNS_TEST_CASES = Page('test_run_test_cases')
ADD_TEST_CASE_TO_TEST_RUN = Page('add_test_case_to_test_run')
LOGIN = Page('login')
