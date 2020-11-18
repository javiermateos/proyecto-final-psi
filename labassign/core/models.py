from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):

    FIRST_NAME_MAX_LENGTH = 128
    LAST_NAME_MAX_LENGTH = 128

    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class TheoryGroup(models.Model):

    GROUP_NAME_MAX_LENGTH = 128
    LANGUAGE_MAX_LENGTH = 128

    groupName = models.CharField(max_length=GROUP_NAME_MAX_LENGTH)
    language = models.CharField(max_length=LANGUAGE_MAX_LENGTH)

    class Meta:
        ordering = ["groupName"]

    def __str__(self):
        return self.groupName


class LabGroup(models.Model):

    GROUP_NAME_MAX_LENGTH = 128
    LANGUAGE_MAX_LENGTH = 128
    SCHEDULE_MAX_LENGTH = 128

    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    groupName = models.CharField(max_length=GROUP_NAME_MAX_LENGTH)
    language = models.CharField(max_length=LANGUAGE_MAX_LENGTH)
    schedule = models.CharField(max_length=SCHEDULE_MAX_LENGTH)
    maxNumberStudents = models.IntegerField()
    counter = models.IntegerField(default=0)

    class Meta:
        ordering = ["groupName"]

    def __str__(self):
        return self.groupName


class GroupConstraints(models.Model):

    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE)

    class Meta:
        ordering = ["labGroup", "theoryGroup"]

    def __str__(self):
        return "{0} {1}".format(self.theoryGroup, self.labGroup)


class Student(User):

    theoryGroup = models.ForeignKey(TheoryGroup,
                                    on_delete=models.PROTECT,
                                    null=True)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.PROTECT, null=True)
    gradeTheoryLastYear = models.FloatField(default=0.0)
    gradeLabLastYear = models.FloatField(default=0.0)
    convalidationGranted = models.BooleanField(default=False)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return "{0} {1}".format(self.last_name, self.first_name)


class Pair(models.Model):
    student1 = models.ForeignKey(Student,
                                 related_name="student1",
                                 on_delete=models.PROTECT)
    student2 = models.ForeignKey(Student,
                                 related_name="student2",
                                 on_delete=models.PROTECT,
                                 null=True)
    studentBreakRequest = models.ForeignKey(
        Student,
        related_name="studentBreakRequest",
        on_delete=models.SET_NULL,
        null=True,
    )
    validated = models.BooleanField(default=False)

    def __str__(self):
        return "{0} {1}".format(self.student1, self.student2)


class OtherConstraints(models.Model):

    selectGroupStartDate = models.DateTimeField()
    minGradeTheoryConv = models.FloatField()
    minGradeLabConv = models.FloatField()

    def __str__(self):
        return "{0} {1} {2}".format(
            self.selectGroupStartDate,
            self.minGradeTheoryConv,
            self.minGradeLabConv,
        )
