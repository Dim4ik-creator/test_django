from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("register/leader/", RegisterLeaderPageView.as_view(), name="leader"),
    path("registe/candidate/", RegisterCandidatePageView.as_view(), name="candidate"),
    path('logout/', logout_view, name='logout'),

    # После входа
    path('home/candidate/', HomeCandidatePageView.as_view(), name='candidate_home'),
    path('home/leader/', HomeLeaderPageView.as_view(), name='leader_home'),

    path("forma/", FormaPageView.as_view(), name="forma"),
    path("about-us", AboutUsPageView.as_view(), name="about-us"),
    path("terms/", TermsPageView.as_view(), name="terms"),
    path("profile/candidate/", ProfCandadatePageView.as_view(), name="profile_candidate"),
    path("profile/leader/", ProfleaderPageView.as_view(), name="profile_leader")
]