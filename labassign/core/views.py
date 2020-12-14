from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.utils import timezone

from core.models import (Student, Pair, OtherConstraints, GroupConstraints,
                         LabGroup)


def home(request):

    context_dict = dict()

    if request.user.is_authenticated:
        student = Student.objects.filter(id=request.user.id).get()
        context_dict['student'] = student
        try:
            pair = Pair.objects.filter(
                Q(student1=student)
                | Q(student2=student, validated=True)).get()
        except ObjectDoesNotExist:
            pair = None
        context_dict['pair'] = pair

    return render(request, 'core/index.html', context=context_dict)


def user_login(request):

    err = None

    if request.user.is_authenticated:
        err = "User already authenticated"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse("index"))
        else:
            err = "Invalid credentials"

    return render(request, 'core/login.html', {"err": err})


@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return redirect(reverse("index"))


def login_help(request):
    return render(request, 'core/login_help.html')


@login_required(login_url="/login/")
def convalidation(request):

    student = Student.objects.filter(id=request.user.id).get()
    gradeTheory = student.gradeTheoryLastYear
    gradeLab = student.gradeLabLastYear
    constraints = OtherConstraints.objects.all().get()

    if (gradeTheory >= constraints.minGradeTheoryConv
            and gradeLab >= constraints.minGradeTheoryConv):
        student.convalidationGranted = True
        student.save()

    context_dict = dict(zip(['student'], [student]))

    return render(request, 'core/convalidation.html', context=context_dict)


def convalidation_help(request):
    return render(request, 'core/convalidation_help.html')


@login_required(login_url="/login/")
def apply_pair(request):

    user1 = Student.objects.filter(id=request.user.id).get()
    students = None
    pair = None
    pair_requested = None
    pair_formed = None

    if request.method == "GET":
        if Pair.objects.filter(student1=user1).exists():
            pair_requested = True
        elif Pair.objects.filter(Q(student1=user1) | Q(student2=user1),
                                 validated=True).exists():
            pair_formed = True

        students = Student.objects.all().exclude(
            Q(id__in=Pair.objects.exclude(validated=False).values('student1'))
            | Q(id__in=Pair.objects.exclude(
                validated=False).values('student2'))
            | Q(id=user1.id))

    if request.method == "POST":
        student2_id = request.POST.get("secondMemberGroup")
        user2 = Student.objects.filter(id=student2_id).get()
        if not Pair.objects.filter(student1=user1).exists():
            try:
                pair = Pair.objects.filter(
                    Q(student1=user1, student2=user2)
                    | Q(student1=user2, student2=user1)).get()
                pair.validated = True
                pair.save()
            except ObjectDoesNotExist:
                pair = Pair.objects.get_or_create(student1=user1,
                                                  student2=user2)[0]
        else:
            pair_requested = True

    context_dict = dict(
        zip(['students', 'pair', 'pair_requested', 'pair_formed'],
            [students, pair, pair_requested, pair_formed]))

    return render(request, 'core/apply_pair.html', context=context_dict)


def applypair_help(request):
    return render(request, 'core/applypair_help.html')


@login_required(login_url="/login/")
def apply_group(request):

    student = Student.objects.filter(id=request.user.id).get()
    try:
        pair = Pair.objects.filter(Q(student1=student) | Q(student2=student),
                                   validated=True).get()
    except ObjectDoesNotExist:
        pair = None

    valid_lab_groups = None
    group_already_selected = None
    group_selected = None
    selection_not_open = None

    if timezone.now() < OtherConstraints.objects.datetimes(
            'selectGroupStartDate', 'day').first():
        selection_not_open = True

    if student.labGroup:
        group_already_selected = True
    else:
        if pair:
            valid_lab_groups = LabGroup.objects.filter(
                id__in=GroupConstraints.objects.filter(
                    theoryGroup=student.theoryGroup,
                    labGroup__in=LabGroup.objects.exclude(
                        counter__gt=F('maxNumberStudents') -
                        2)).values('labGroup'))
        else:
            valid_lab_groups = LabGroup.objects.filter(
                id__in=GroupConstraints.objects.filter(
                    theoryGroup=student.theoryGroup,
                    labGroup__in=LabGroup.objects.exclude(
                        counter=F('maxNumberStudents'))).values('labGroup'))

    if request.method == "POST":
        groupName = request.POST.get("myLabGroup")
        labgroup = LabGroup.objects.filter(groupName=groupName).get()
        if labgroup in valid_lab_groups:
            labgroup.counter += 1
            student.labGroup = labgroup
            student.save()
            if pair:
                if (pair.student1 == student):
                    student2 = pair.student2
                else:
                    student2 = pair.student1
                labgroup.counter += 1
                student2.labGroup = labgroup
                student2.save()
            labgroup.save()
            group_selected = True

    context_dict = dict(
        zip([
            'student', 'labGroups', 'group_already_selected', 'group_selected',
            'selection_not_open'
        ], [
            student, valid_lab_groups, group_already_selected, group_selected,
            selection_not_open
        ]))

    return render(request, 'core/apply_group.html', context=context_dict)


def applygroup_help(request):
    selectGroupStartDate = OtherConstraints.objects.get().selectGroupStartDate
    currentDate = timezone.now

    context_dict = dict(zip(['selectGroupStartDate', 'currentDate'],
                            [selectGroupStartDate, currentDate]))

    return render(request, 'core/applygroup_help.html', context=context_dict)


def breakpair_help(request):
    render(request, 'core/breakpair_help.html')


@login_required(login_url="/login/")
def breakpair(request):
    processed = -1
    student = Student.objects.filter(id=request.user.id).get()

    pairs = Pair.objects.filter(Q(student1=student) | Q(student2=student))

    if request.method == 'POST':
        pair_id = request.POST.get('myPair')
        processed = 2
        if Pair.objects.filter(id=pair_id).exists():
            pair = Pair.objects.filter(id=pair_id).get()
            if pair.validated is False:
                pair.delete()
                processed = 0
            else:
                if pair.studentBreakRequest is None:
                    pair.studentBreakRequest = student
                    pair.save()
                    processed = 1
                else:
                    if student == pair.studentBreakRequest:
                        processed = 2
                    else:
                        pair.delete()
                        processed = 0

    context_dict = dict(zip(['student', 'pairs', 'processed'],
                            [student, pairs, processed]))

    return render(request, 'core/break_pair.html', context_dict)
