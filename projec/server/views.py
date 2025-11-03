from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView, CreateView, FormView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import *
from .forms import *
from .mixins import *


class HomePageView(TemplateView):
    template_name = "index.html"


class LoginPageView(FormView):
    template_name = "login.html"
    success_url = reverse_lazy("home")
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        # Проверяем кандидата
        candidate = Candidante.objects.filter(email=email).first()
        if candidate:
            if candidate.is_banned:
                messages.error(
                    self.request,
                    f"Ваш аккаунт заблокирован по причине: {candidate.ban_reason}",
                )
                return redirect("login")
            if check_password(password, candidate.password):
                self.request.session["user_type"] = "candidate"
                self.request.session["user_name"] = candidate.name
                self.request.session["user_email"] = candidate.email
                return redirect("candidate_home")

        # Проверяем руководителя
        leader = Leader.objects.filter(email=email).first()
        if leader:
            if leader.is_banned:
                messages.error(
                    self.request,
                    f"Ваш аккаунт заблокирован по причине: {leader.ban_reason}",
                )
                return redirect("login")
            if check_password(password, leader.password):
                self.request.session["user_type"] = "leader"
                self.request.session["user_name"] = leader.name
                self.request.session["user_email"] = leader.email
                self.request.session["user_company"] = leader.company
                self.request.session["user_company_city"] = leader.city
                return redirect("leader_home")

        return self.form_invalid(form)


class HomeCandidatePageView(CandidateOnlyMixin, TemplateView):
    model = Candidante
    template_name = "home_candidate.html"
    fields = "__all__"
    login_url = "login"
    redirect_field_name = None


class HomeLeaderPageView(LeaderOnlyMixin, TemplateView):
    model = Leader
    template_name = "home_leader.html"
    fields = "__all__"
    login_url = "login"
    redirect_field_name = None


# Профиль для кандидата
class ProfCandidatePageView(CandidateOnlyMixin, TemplateView):
    model = Candidante
    template_name = "profile_candidate.html"
    fields = "__all__"
    login_url = "login"
    redirect_field_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем текущего кандидата из БД по пользователю
        candidante_email = self.request.session.get("user_email")
        candidate = Candidante.objects.filter(email=candidante_email).first()
        context['candidate'] = candidate
        return context
    

class EditCandidateProfileView(CandidateOnlyMixin, View):

    def post(self, request):
        email = request.session.get("user_email")
        candidate = Candidante.objects.filter(email=email).first()

        if candidate:
            candidate.name = request.POST.get("name")
            candidate.email = request.POST.get("email")
            # candidate.skills = request.POST.get("skills")
            # candidate.experience = request.POST.get("experience")
            candidate.save()
            messages.success(request, "Профиль успешно обновлён!")

        return redirect("profile_candidate")


# Профиль для руководителя
class ProfleaderPageView(LeaderOnlyMixin, UpdateView):
    model = Leader
    template_name = "profile_leader.html"
    fields = "__all__"
    login_url = "login"
    redirect_field_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем текущего лидера из БД по пользователю
        leader_email = self.request.session.get("user_email")
        leader = Leader.objects.filter(email=leader_email).first()
        context['leader'] = leader
        return context
    

class EditLeaderProfileView(CandidateOnlyMixin, UpdateView):
    model = Candidante
    template_name = "edit_profile_leader.html"
    success_url = reverse_lazy("profile_leader")

    def get_object(self, queryset = None):
        email = self.request.session.get("user_email")
        return Leader.objects.filter(email=email).first()


class RegisterCandidatePageView(CreateView):
    model = Candidante
    template_name = "register_candidate.html"
    form_class = RegisterCandidanteForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)


class RegisterLeaderPageView(CreateView):
    model = Leader
    template_name = "register_leader.html"
    form_class = RegisterLeaderForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)


class FormaPageView(View):
    template_name = "forma.html"

    def get(self, request):
        context = {
            "name": request.session.get("contact_name", ""),
            "email": request.session.get("contact_email", ""),
            "message": request.session.get("contact_message", ""),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # сохраняем в сессию
        request.session["contact_name"] = name
        request.session["contact_email"] = email
        request.session["contact_message"] = message
        if not name or not email or not message:
            return render(
                request,
                self.template_name,
                {
                    "error": "Все поля обязательны для заполнения.",
                    "name": name,
                    "email": email,
                    "message": message,
                },
            )

        try:
            email_message = EmailMessage(
                subject=f"Сообщение с сайта от {name}",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[email],
            )

            email_message.send(fail_silently=False)

            # очищаем сессию после успешной отправки
            for key in ("contact_name", "contact_email", "contact_message"):
                request.session.pop(key, None)

            return render(request, self.template_name, {"success": True})

        except Exception as e:
            return render(
                request,
                self.template_name,
                {
                    "error": f"Ошибка при отправке письма: {e}",
                    "name": name,
                    "email": email,
                    "message": message,
                },
            )


# Страница о нас
class AboutUsPageView(TemplateView):
    template_name = "about_us.html"


# Страница формы(обратной связи)
class TermsPageView(TemplateView):
    template_name = "terms.html"


# Функция для выхода из аккаунта
def logout_view(request):
    request.session.flush()
    return redirect("home")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не определена</h1>")
