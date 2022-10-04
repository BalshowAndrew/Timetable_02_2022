from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import *
from .models import Classes, Queries


def index(request):
    context = {
        'title': 'Расписание кафедры',
    }
    return render(request, 'classes/index.html', context=context)


def show_person(request):
    context = {
        'title': 'Личный кабинет',
    }
    return render(request, 'classes/person.html', context=context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'classes/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('person')


def logout_user(request):
    logout(request)
    return redirect('home')


def get_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result')
    else:
        form = QueryForm()
    return render(request, 'classes/query.html', {'form': form})


def get_result(request):
    query = Queries.objects.order_by('pk').last()
    if query.category == 'P':
        result = Classes.objects.filter(
            teacher_id=request.user.pk,
            category='P'
        )
    elif query.category == 'L':
        result = Classes.objects.filter(
            teacher_id=request.user.pk,
            category='L'
        )


    context = {
        'query': query,
        'result': result,
        'title': 'Результат запроса',

    }
    return render(request, 'classes/result.html', context=context)
