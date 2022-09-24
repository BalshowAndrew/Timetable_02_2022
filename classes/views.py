from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import QueryForm


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
    form_class = AuthenticationForm
    template_name = 'classes/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('person')

def logout_user(request):
    logout(request)
    return redirect('home')


def get_query(request):
    # context = {'title': 'Форма запроса',
    #            }
    if request.method == 'POST':
        pass
    else:
        form = QueryForm()
    return render(request, 'classes/query.html', {'form': form})