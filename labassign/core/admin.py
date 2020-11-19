from django.contrib import admin

from core.models import (
    Teacher,
    LabGroup,
    TheoryGroup,
    GroupConstraints,
    Student,
    Pair,
    OtherConstraints,
)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")


class TheoryGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "groupName", "language")


class LabGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "teacher", "groupName", "language", "schedule",
                    "maxNumberStudents", "counter")


class GroupConstraintsAdmin(admin.ModelAdmin):
    list_display = ("id", "theoryGroup", "labGroup")


class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "labGroup", "theoryGroup", "first_name", "last_name",
                    "username", "password", "gradeTheoryLastYear",
                    "gradeLabLastYear", "convalidationGranted")


class PairAdmin(admin.ModelAdmin):
    list_display = ("id", "student1", "student2", "studentBreakRequest",
                    "validated")


class OtherConstraintsAdmin(admin.ModelAdmin):
    list_display = ("selectGroupStartDate", "minGradeTheoryConv",
                    "minGradeLabConv")


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TheoryGroup, TheoryGroupAdmin)
admin.site.register(LabGroup, LabGroupAdmin)
admin.site.register(GroupConstraints, GroupConstraintsAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Pair, PairAdmin)
admin.site.register(OtherConstraints, OtherConstraintsAdmin)
