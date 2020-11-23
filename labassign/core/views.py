from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from core.models import (Student, Pair, OtherConstraints, GroupConstraints, LabGroup)


def home(request):

    context_dict = dict()

    if request.user.is_authenticated:
        student = Student.objects.filter(id=request.user.id).get()
        context_dict['student'] = student
        try:
            pair = Pair.objects.filter(
                Q(student1=student)
                | Q(student2=student)).get()
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

    if request.method == "POST":
        student2_id = request.POST.get("secondMemberGroup")
        user2 = Student.objects.filter(id=student2_id).get()
        pair, created = Pair.objects.get_or_create(student1=user1,
                                                   student2=user2)
        if created is False:
            pair.validated = True

    students = Student.objects.all().exclude(
        Q(id__in=Pair.objects.exclude(validated=False).values('student1'))
        | Q(id__in=Pair.objects.exclude(validated=False).values('student2'))
        | Q(id=user1.id))

    context_dict = dict(zip(['students'], [students]))

    return render(request, 'core/apply_pair.html', context=context_dict)


def applypair_help(request):
    return render(request, 'core/applypair_help.html')


@login_required(login_url="/login/")
def apply_group(request):

    student = Student.objects.filter(id=request.user.id).get()
    theory_group = student.theoryGroup
    available_groups = GroupConstraints.objects.filter(theoryGroup = theory_group)
    try:
        validated_pair = Pair.objects.filter(validated = True).filter(
            Q(student1 = student) | Q(student2 = student)
        ).get()
    except:
        validated_pair = None

    valid_lab_groups = []
    if validated_pair == None: 
        for g in available_groups:
            if g.labGroup.maxNumberStudents > g.labGroup.counter:
                valid_lab_groups.append(g.labGroup)
    else:
        for g in available_groups:
            if g.labGroup.maxNumberStudents > (g.labGroup.counter + 1):
                valid_lab_groups.append(g.labGroup)


    if request.method == "POST":
        if validated_pair == None:
            lab_group = LabGroup.objects.filter(id = request.POST.get("lab-group")).get()
            lab_group.counter += 1
            student.labGroup = lab_group
            student.save()
            lab_group.save()

    context_dict = dict(zip(['labGroups'], [valid_lab_groups]))
 
    return render(request, 'core/apply_group.html', context=context_dict)


def applygroup_help(request):
    keys = ['selectGroupStartDate', 'currentDate']
    # TODO: Sustituir los valores por una lista
    context_dict = dict(zip(keys, [None] * len(keys)))
    return render(request, 'core/applygroup_help.html', context=context_dict)


@login_required(login_url="/login/")
def break_pair(request):
    return render(request, 'core/break_pair.html')
