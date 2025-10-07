from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .forms import LoginForm


class HomePageView(TemplateView):
    template_name = "index.html"


class LoginPageView(FormView):
    template_name = "login.html"
    success_url = reverse_lazy('home')
    form_class = LoginForm


    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Проверяем кандидата
        candidate = Candidante.objects.filter(email=email).first()
        if candidate and check_password(password, candidate.password):
            self.request.session['user_type'] = 'candidate'
            self.request.session['user_name'] = candidate.name
            return redirect('candidate_home')

        # Проверяем руководителя
        leader = Leader.objects.filter(email=email).first()
        if leader and check_password(password, leader.password):
            self.request.session['user_type'] = 'leader'
            self.request.session['user_name'] = leader.name
            return redirect('leader_home')

        # Если не найден
        return self.form_invalid(form)


class HomeCandidatePageView(TemplateView):
    model = Candidante
    template_name = 'home_candidate.html'
    fields = '__all__'


class HomeLeaderPageView(TemplateView):
    model = Candidante
    template_name = 'home_leader.html'
    fields = '__all__'


class RegisterCandidatePageView(CreateView):
    model = Candidante
    template_name = "register_candidate.html"
    fields = '__all__'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)

class RegisterLeaderPageView(CreateView):
    model = Leader
    template_name = "register_leader.html"
    fields = '__all__'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)




def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не определена</h1>")