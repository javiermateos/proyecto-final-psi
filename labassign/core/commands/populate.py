# Populate database
# This file has to be placed within the
# core/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate


from django.core.management.base import BaseCommand
from ..models import (
    OtherConstraints,
    Pair,
    Student,
    GroupConstraints,
    TheoryGroup,
    LabGroup,
    Teacher,
)

from datetime import datetime, timedelta

import csv


# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
#
# Teachers, groups and constraints
# will be hardcoded in this file.
# Students will be read from a cvs file
# last year grade will be obtained from another cvs file
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate database
           """
    teachers = list()
    labgroups = list()
    theorygroups = list()
    students = list()

    def add_arguments(self, parser):
        parser.add_argument(
            "model",
            type=str,
            help="""
        model to  update:
        all -> all models
        teacher
        labgroup
        theorygroup
        groupconstraints
        otherconstrains
        student (require csv file)
        studentgrade (require different csv file,
        update only existing students)
        pair
        """,
        )
        parser.add_argument(
            "studentinfo",
            type=str,
            help="""CSV file with student information
        header= NIE, DNI, Apellidos, Nombre, Teoría
        if NIE or DNI == 0 skip this entry and print a warning""",
        )
        parser.add_argument(
            "studentinfolastyear",
            type=str,
            help="""CSV file with student information
        header= NIE,DNI,Apellidos,Nombre,Teoría, grade lab, grade the
        if NIE or DNI == 0 skip this entry and print a warning""",
        )

    # handle is another compulsory name, do not change it"
    def handle(self, *args, **kwargs):
        model = kwargs["model"]
        cvsStudentFile = kwargs["studentinfo"]
        cvsStudentFileGrades = kwargs["studentinfolastyear"]
        # clean database
        if model == "all":
            self.cleanDataBase()
        if model == "teacher" or model == "all":
            self.teacher()
        if model == "labgroup" or model == "all":
            self.labgroup()
        if model == "theorygroup" or model == "all":
            self.theorygroup()
        if model == "groupconstraints" or model == "all":
            self.groupconstraints()
        if model == "otherconstrains" or model == "all":
            self.otherconstrains()
        if model == "student" or model == "all":
            self.student(cvsStudentFile)
        if model == "studentgrade" or model == "all":
            self.studentgrade(cvsStudentFileGrades)
        if model == "pair" or model == "all":
            self.pair()

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        Teacher.obejects.all().delete
        LabGroup.obejects.all().delete
        TheoryGroup.obejects.all().delete
        LabGroup.obejects.all().delete
        GroupConstraints.obejects.all().delete
        Student.obejects.all().delete
        Pair.obejects.all().delete

    def teacher(self):
        "create teachers here"
        teachersDict = [
            {"first_name": "Santiago", "last_name": "Abascal"},
            {"first_name": "Pablo", "last_name": "Iglesias"},
            {"first_name": "Pedro", "last_name": "Sanchez"},
            {"first_name": "Pablo", "last_name": "Casado"},
            {"first_name": "Javier", "last_name": "Sanchez"},
            {"first_name": "Ines", "last_name": "Arrimadas"},
            {"first_name": "Aitor", "last_name": "Esteban"},
            {"first_name": "Gabriel", "last_name": "Rufian"},
        ]

        for t in teachersDict:
            element = Teacher.objects.get_or_create(
                firs_name=t["firstname"], last_name=t["last_name"]
            )
            element.save()
            self.teachers.append(element)

    def labgroup(self):
        "add labgroups"
        labGoupsDict = [
            {
                "groupName": "1261",
                "language": "spanish",
                "schedule": "9-11",
                "maxNumberStudents": 20,
            },
            {
                "groupName": "1262",
                "language": "spanish",
                "schedule": "9-11",
                "maxNumberStudents": 20,
            },
            {
                "groupName": "1263",
                "language": "spanish",
                "schedule": "9-11",
                "maxNumberStudents": 20,
            },
            {
                "groupName": "1271",
                "language": "spanish",
                "schedule": "11-13",
                "maxNumberStudents": 20,
            },
            {
                "groupName": "1272",
                "language": "spanish",
                "schedule": "11-13",
                "maxNumberStudents": 20,
            },
            {
                "groupName": "1201",
                "language": "english",
                "schedule": "11-13",
                "maxNumberStudents": 20,
            },
            {
                "groupName": "1291",
                "language": "spanish",
                "schedule": "11-13",
                "maxNumberStudents": 20,
            },
            {
                "groupName": "1292",
                "language": "spanish",
                "schedule": "11-13",
                "maxNumberStudents": 20,
            },
        ]

        i = 0
        for lg in labGoupsDict:
            element = LabGroup.objects.get_or_create(
                teacher=self.teachers[i],
                groupName=lg["groupName"],
                language=lg["language"],
                schedule=lg["schedule"],
                maxNumberStudents=lg["maxNumberStudents"],
            )
            element.save()
            self.labgroups.append(element)
            i += 1

    def theorygroup(self):
        "add theorygroups"
        theoryGroupsDict = [
            {"groupName": "126", "language": "spanish"},
            {"groupName": "127", "language": "spanish"},
            {"groupName": "120", "language": "english"},
            {"groupName": "129", "language": "spanish"},
            {"groupName": "125", "language": "spanish"},
        ]

        for tg in theoryGroupsDict:
            element = TheoryGroup.objects.get_or_create(
                groupName=tg["gropuName"], language=tg["language"]
            )
            element.save()
            self.theorygroups.append(element)

    def groupconstraints(self):
        "add group constrints"
        """ Follows which laboratory groups (4th column
            may be choosen by which theory groups (2nd column)
            theoryGroup: 126, labGroup: 1261
            theoryGroup: 126, labGroup: 1262
            theoryGroup: 126, labGroup: 1263
            theoryGroup: 127, labGroup: 1271
            theoryGroup: 127, labGroup: 1272
            theoryGroup: 120, labGroup: 1201
            theoryGroup: 129, labGroup: 1291
            theoryGroup: 125, labGroup: 1252"""

        for tg in self.theorygroups:
            for lg in self.labgroups:
                if lg.get("groupName").startswith(tg.get("groupName")):
                    element = GroupConstraints.objects.get_or_create(
                        theoryGroup=tg, labGroup=lg
                    )
                    element.save()


    def pair(self):
        "create a few valid pairs"
        for i in range(2):
            element = Pair.objects.get_or_create(
                student1=self.students[i],
                student2=self.students[-i],
                validated=True
            )
            element.save()


    def otherconstrains(self):
        """create a single object here with staarting dates
        and maximum and minimum convalidation grades"""
        """ Use the following values:
        selectGroupStartDate = now + 1 day,
        minGradeTheoryConv = 3,
        minGradeLabConv = 7
        """
        OtherConstraints.objects.get_or_create(
            selectGroupstartDate=datetime.now() + timedelta(1),
            minGradeTheoryConv=3,
            minGradeLabConv=7,
        )

    def student(self, csvStudentFile):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría
        new_students_dict = csv.DictReader(csvStudentFile)

        for s in new_students_dict:
            Student.objects.get_or_create(
                username=s["NIE"],
                password=s["DNI"],
                last_name=s["Apellidos"],
                first_name=s["Nombre"],
                theoryGroup=self.theorygroups[self.theorygroups.index(s["grupo-teoria"])],
            )

    def studentgrade(self, cvsStudentFileGrades):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría	grade-practicas
        # gradeteoria
        old_students_dict = csv.DictReader(cvsStudentFileGrades)

        for s in old_students_dict:
            Student.objects.get_or_create(
                username=s["NIE"],
                password=s["DNI"],
                last_name=s["Apellidos"],
                first_name=s["Nombre"],
                theoryGroup=self.theorygroups[self.theorygroups.index(s["grupo-teoria"])],
                gradeTheoryLastYear=float(s["nota-teoria"]),
                gradeLabLastYear=float(s["nota-practicas"]),
            )
