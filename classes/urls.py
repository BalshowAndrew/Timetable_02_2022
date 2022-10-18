from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('person/', show_person, name='person'),
    path('login/', LoginUser.as_view(), name='login'),
    path('login/login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('person/logout/', logout_user, name='logout'),
    path('login/logout/', logout_user, name='logout'),
    path('person/query/logout/', logout_user, name='logout'),
    path('person/query/result/logout/', logout_user, name='logout'),
    path('person/query/', get_query, name='query'),
    path('person/query/result/', get_result, name='result'),
    path('result_csv/', result_csv, name='result_csv'),
    path('result_pdf/', result_pdf, name='result_pdf'),
]
