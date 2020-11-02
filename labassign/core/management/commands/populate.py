# Populate database
# This file has to be placed within the
# core/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate


from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from ...models import (
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
from collections import OrderedDict


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
        Teacher.objects.all().delete
        LabGroup.objects.all().delete
        TheoryGroup.objects.all().delete
        LabGroup.objects.all().delete
        GroupConstraints.objects.all().delete
        Student.objects.all().delete
        Pair.objects.all().delete

    def teacher(self):
        "create teachers here"
        teachersDict = [
            {"first_name": "No", "last_name": "Asignado1"},
            {"first_name": "No", "last_name": "Asignado4"},
            {"first_name": "Julia", "last_name": "Diaz Garcia"},
            {"first_name": "Alvaro", "last_name": "del Val Latorre"},
            {"first_name": "Roberto", "last_name": "Marabini Ruiz"},
        ]

        for t in teachersDict:
            element = Teacher.objects.get_or_create(
                first_name=t["first_name"], last_name=t["last_name"]
            )[0]
            element.save()

    def labgroup(self):
        "add labgroups"
        labGroupsDict = [
            {
                "id": 1261,
                "teacher": Teacher.objects.get(
                    first_name="No", last_name="Asignado1"),
                "groupName": "1261",
                "language": "español/Spanish",
                "schedule": "Lunes/Monday 18-20",
                "maxNumberStudents": 23,
            },
            {
                "id": 1262,
                "teacher": Teacher.objects.get(
                    first_name="No", last_name="Asignado4"),
                "groupName": "1262",
                "language": "español/Spanish",
                "schedule": "Miércoles/Wednesday 18-20",
                "maxNumberStudents": 23,
            },
            {
                "id": 1263,
                "teacher": Teacher.objects.get(
                    first_name="No", last_name="Asignado4"),
                "groupName": "1263",
                "language": "español/Spanish",
                "schedule": "Viernes/Friday 17-19",
                "maxNumberStudents": 23,
            },
            {
                "id": 1271,
                "teacher": Teacher.objects.get(
                    first_name="No", last_name="Asignado1"),
                "groupName": "1271",
                "language": "español/Spanish",
                "schedule": "Miércoles/Wednesday 18-20",
                "maxNumberStudents": 23,
            },
            {
                "id": 1272,
                "teacher": Teacher.objects.get(
                    first_name="Julia", last_name="Diaz Garcia"),
                "groupName": "1272",
                "language": "español/Spanish",
                "schedule": "Viernes/Friday 17-19",
                "maxNumberStudents": 23,
            },
            {
                "id": 1201,
                "teacher": Teacher.objects.get(
                    first_name="Roberto", last_name="Marabini Ruiz"),
                "groupName": "1201",
                "language": "español/Spanish",
                "schedule": "Miércoles/Wednesday 18-20",
                "maxNumberStudents": 23,
            },
            {
                "id": 1291,
                "teacher": Teacher.objects.get(
                    first_name="Julia", last_name="Diaz Garcia"),
                "groupName": "1291",
                "language": "inglés/English",
                "schedule": "Lunes/Monday 18-20",
                "maxNumberStudents": 23,
            },
            {
                "id": 1292,
                "teacher": Teacher.objects.get(
                    first_name="Alvaro", last_name="del Val Latorre"),
                "groupName": "1292",
                "language": "inglés/English",
                "schedule": "Viernes/Friday 17-19",
                "maxNumberStudents": 23,
            },
        ]

        for lg in labGroupsDict:
            element = LabGroup.objects.get_or_create(
                id=lg["id"],
                teacher=lg["teacher"],
                groupName=lg["groupName"],
                language=lg["language"],
                schedule=lg["schedule"],
                maxNumberStudents=lg["maxNumberStudents"],
            )[0]
            element.save()

    def theorygroup(self):
        "add theorygroups"
        theoryGroupsDict = [
            {"id": 126, "groupName": "126", "language": "español/Spanish"},
            {"id": 127, "groupName": "127", "language": "español/Spanish"},
            {"id": 120, "groupName": "120", "language": "español/Spanish"},
            {"id": 129, "groupName": "129", "language": "inglés/English"},
            {"id": 125, "groupName": "125", "language": "inglés/English"},
        ]

        for tg in theoryGroupsDict:
            element = TheoryGroup.objects.get_or_create(
                id=tg["id"], groupName=tg["groupName"], language=tg["language"]
            )[0]
            element.save()

    def groupconstraints(self):
        "add group constrints"
        """
        Follows which laboratory groups (4th column
            may be choosen by which theory groups (2nd column)
            theoryGroup: 126, labGroup: 1261
            theoryGroup: 126, labGroup: 1262
            theoryGroup: 126, labGroup: 1263
            theoryGroup: 127, labGroup: 1271
            theoryGroup: 127, labGroup: 1272
            theoryGroup: 120, labGroup: 1201
            theoryGroup: 129, labGroup: 1291
            theoryGroup: 125, labGroup: 1292
        """

        groupConstraintsDict = [
            {"theoryGroup": TheoryGroup.objects.get(groupName="120"),
             "labGroup": LabGroup.objects.get(groupName="1201")},
            {"theoryGroup": TheoryGroup.objects.get(groupName="126"),
             "labGroup": LabGroup.objects.get(groupName="1261")},
            {"theoryGroup": TheoryGroup.objects.get(groupName="126"),
             "labGroup": LabGroup.objects.get(groupName="1262")},
            {"theoryGroup": TheoryGroup.objects.get(groupName="126"),
             "labGroup": LabGroup.objects.get(groupName="1263")},
            {"theoryGroup": TheoryGroup.objects.get(groupName="127"),
             "labGroup": LabGroup.objects.get(groupName="1271")},
            {"theoryGroup": TheoryGroup.objects.get(groupName="127"),
             "labGroup": LabGroup.objects.get(groupName="1272")},
            {"theoryGroup": TheoryGroup.objects.get(groupName="129"),
             "labGroup": LabGroup.objects.get(groupName="1291")},
            {"theoryGroup": TheoryGroup.objects.get(groupName="125"),
             "labGroup": LabGroup.objects.get(groupName="1292")},
        ]

        for gc in groupConstraintsDict:
            element = GroupConstraints.objects.get_or_create(
                theoryGroup=gc["theoryGroup"], labGroup=gc["labGroup"]
            )[0]
            element.save()

    def pair(self):
        "create a few valid pairs"

        pairD = OrderedDict()
        pairD[1000] = {'student2': 1100, 'validated': False}
        pairD[1001] = {'student2': 1101, 'validated': False}
        pairD[1010] = {'student2': 1110, 'validated': True}
        pairD[1011] = {'student2': 1111, 'validated': True}
        pairD[1012] = {'student2': 1112, 'validated': True}

        for p in pairD.keys():
            element = Pair.objects.get_or_create(
                student1=Student.objects.get(id=p),
                student2=Student.objects.get(id=pairD.get(p)["student2"]),
                validated=pairD.get(p)["validated"]
            )[0]
            element.save()

    def otherconstrains(self):
        """create a single object here with staarting dates
        and maximum and minimum convalidation grades"""
        """ Use the following values:
        selectGroupStartDate = now + 1 day,
        minGradeTheoryConv = 3,
        minGradeLabConv = 7
        """
        element = OtherConstraints.objects.get_or_create(
            selectGroupStartDate=make_aware(
                datetime.now() + timedelta(days=1)),
            minGradeTheoryConv=3,
            minGradeLabConv=7,
        )[0]
        element.save()

    def student(self, csvStudentFile):
        # structure NIE	DNI	Apellidos Nombre group-Teoría
        with open(csvStudentFile) as csv_file:
            new_students_dict = csv.DictReader(csv_file)
            counter = 1000
            for s in new_students_dict:
                element = Student.objects.get_or_create(
                    id=counter,
                    username=s["NIE"],
                    password=s["DNI"],
                    last_name=s["Apellidos"],
                    first_name=s["Nombre"],
                    theoryGroup=TheoryGroup.objects.get(
                        groupName=s["grupo-teoria"]
                    ),
                )[0]
                element.save()
                counter += 1
            print(counter)

    def studentgrade(self, csvStudentFileGrades):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría	grade-practicas
        # gradeteoria
        with open(csvStudentFileGrades) as csv_file:
            old_students_dict = csv.DictReader(csv_file)
            for s in old_students_dict:
                defaults = {
                    "gradeTheoryLastYear": float(s["nota-teoria"]),
                    "gradeLabLastYear": float(s["nota-practicas"])
                }
                element = Student.objects.update_or_create(
                    username=s["NIE"],
                    password=s["DNI"],
                    last_name=s["Apellidos"],
                    first_name=s["Nombre"],
                    theoryGroup=TheoryGroup.objects.get(
                        groupName=s["grupo-teoria"]
                    ),
                    defaults=defaults
                )[0]
                element.save()
