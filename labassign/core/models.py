from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):

    FIRST_NAME_MAX_LENGTH = 128
    LAST_NAME_MAX_LENGTH = 128

    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH)

    class Meta:
        # Orden alfabético
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class TheoryGroup(models.Model):

    GROUP_NAME_MAX_LENGTH = 128
    LANGUAGE_MAX_LENGTH = 128

    groupName = models.CharField(max_length=GROUP_NAME_MAX_LENGTH)
    language = models.CharField(LANGUAGE_MAX_LENGTH)

    class Meta:
        # Orden albético
        ordering = ["group_name"]

    def __str__(self):
        return self.group_name


class LabGroup(models.Model):

    GROUP_NAME_MAX_LENGTH = 128
    LANGUAGE_MAX_LENGTH = 128
    SCHEDULE_MAX_LENGTH = 128

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groupName = models.CharField(max_length=GROUP_NAME_MAX_LENGTH)
    language = models.CharField(max_length=LANGUAGE_MAX_LENGTH)
    schedule = models.CharField(max_length=SCHEDULE_MAX_LENGTH)
    maxNumberStudents = models.IntegerField()
    counter = models.IntegerField()

    class Meta:
        # Orden albético
        ordering = ["group_name"]

    def __str__(self):
        return self.groupName


class GroupConstraints(models.Model):

    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE)

    class Meta:
        # Orden albético
        ordering = [TheoryGroup.group_name, LabGroup.groupName]

    def __str__(self):
        return self.theoryGroup + " " + self.labGroup


class Student(User):

    labGroup = models.ForeignKey(LabGroup, on_delete=models.PROTECT)
    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.PROTECT)
    gradeTheoryLastYear = models.FloatField()
    gradeLabLastYear = models.FloatField()
    convalidationGranted = models.BooleanField(default=False)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.username


class Pair(models.Model):

    student1 = models.ForeignKey(Student, on_delete=models.PROTECT)
    student2 = models.ForeignKey(
        Student, on_delete=models.PROTECT, null=True, blank=True
    )
    studentBreakRequest = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True, blank=True
    )
    validated = models.Boolean(default=False)

    def __str__(self):
        return self.student1 + " " + self.student2


class OtherConstraints(models.Model):

    selectGroupStartDate = models.DateTimeField()
    minGradeTheoryConv = models.FloatField()
    minGradeLabConv = models.FloatField()

    def __str__(self):
        return self.selectGroupStartDate
