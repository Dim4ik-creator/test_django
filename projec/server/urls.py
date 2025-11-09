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
    path("profile/candidate/", ProfCandidatePageView.as_view(), name="profile_candidate"),
    path("profile/leader/", ProfleaderPageView.as_view(), name="profile_leader"),

    path("profile/candidate/edit/", EditCandidateProfileView.as_view(), name="edit_profile_candidate"),
    path("profile/leader/edit/", EditLeaderProfileView.as_view(), name="edit_profile_leader"),
    # Вакансии
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/create/', JobCreateView.as_view(), name='create_job'),
    path('jobs/my/', MyJobsView.as_view(), name='my_jobs'),
    path('jobs/<int:job_id>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/<int:job_id>/responses', ResponceView.as_view(), name='view_responses'),
]
