from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)


class Release(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField(unique=True, null=False)
    description = models.TextField(null=True)


class TestPlan(models.Model):
    release = models.OneToOneField(Release, on_delete=models.CASCADE)


class TestCase(models.Model):
    description = models.TextField()
    expectedResult = models.CharField(max_length=200)


class TestRun(models.Model):
    testPlan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    testCase = models.ManyToManyField(TestCase, blank=True)


class TestRunResult(models.Model):
    testRun = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    testPlan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    runDate = models.DateTimeField()
    successfulTestes = models.IntegerField()
    failedTestes = models.IntegerField()
    progress = models.FloatField()  # percent
    isFinished = models.BooleanField()


class TestCaseResult(models.Model):
    testCase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    testRun = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    testRunResult = models.ForeignKey(TestRunResult, on_delete=models.CASCADE)
    isSuccessful = models.BooleanField()
    runDate = models.DateTimeField()
    realResult = models.CharField(max_length=200)
