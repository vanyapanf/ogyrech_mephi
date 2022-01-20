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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_id')
    testCase = models.ManyToManyField(TestCase, blank=True)
    creator = models.ForeignKey(User, related_name='creator_id', on_delete=models.DO_NOTHING)


class TestRunResult(models.Model):
    testRun = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    testPlan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    runDate = models.DateTimeField(auto_now_add=True)
    successfulTestes = models.IntegerField(default=0)
    failedTestes = models.IntegerField(default=0)
    progress = models.FloatField(default=0.0)  # percent
    isFinished = models.BooleanField(default=False)


class TestCaseResult(models.Model):
    testCase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    testRun = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    testRunResult = models.ForeignKey(TestRunResult, on_delete=models.CASCADE)
    isSuccessful = models.BooleanField()
    runDate = models.DateTimeField()
    realResult = models.CharField(max_length=200)


class TaskSystem(models.Model):
    hostName = models.CharField(max_length=200, unique=True)
