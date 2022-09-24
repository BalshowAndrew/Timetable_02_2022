from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('person/', show_person, name='person'),
    path('login/', LoginUser.as_view(), name='login'),
    path('person/logout/', logout_user, name='logout'),
    path('person/query/logout/', logout_user, name='logout'),
    path('person/query/', get_query, name='query'),
]