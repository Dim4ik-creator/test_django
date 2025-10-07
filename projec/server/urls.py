from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("register/leader/", RegisterLeaderPageView.as_view(), name="leader"),
    path("registe/candidate/", RegisterCandidatePageView.as_view(), name="candidate"),

    # После входа
    path('home/candidate/', HomeCandidatePageView.as_view(), name='candidate_home'),
    path('home/leader/', HomeLeaderPageView.as_view(), name='leader_home'),
]