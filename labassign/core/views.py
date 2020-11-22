from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from core.models import (Student, Pair, OtherConstraints)


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

    students = Student.objects.all().exclude(id__in=Pair.objects.exclude(
        validated=False).only('student1'))

    print(students)

    return render(request, 'core/apply_pair.html')


def applypair_help(request):
    return render(request, 'core/applypair_help.html')


@login_required(login_url="/login/")
def apply_group(request):
    return render(request, 'core/apply_group.html')


def applygroup_help(request):
    keys = ['selectGroupStartDate', 'currentDate']
    # TODO: Sustituir los valores por una lista
    context_dict = dict(zip(keys, [None] * len(keys)))
    return render(request, 'core/applygroup_help.html', context=context_dict)


@login_required(login_url="/login/")
def break_pair(request):
    return render(request, 'core/break_pair.html')
