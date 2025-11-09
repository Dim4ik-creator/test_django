from django.contrib import admin
from django.shortcuts import redirect, render
from django.utils.html import format_html
from django.urls import path
from .models import *
from .forms import *


def ban_selected_users(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = BanUserForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            days = form.cleaned_data['days']
            for user in queryset:
                user.is_banned = True
                user.ban_reason = reason
                user.ban_until = timezone.now() + timedelta(days=days)
                user.save()
            modeladmin.message_user(request, f"{queryset.count()} пользователей забанено")
            return None
    else:
        form = BanUserForm()
    return render(request, 'admin/ban_users.html', {'users': queryset, 'form': form, 'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,})


def ban_selected(modeladmin, request, queryset):
    queryset.update(is_banned=True)
ban_selected.short_description = "Забанить выбранных пользователей"

def unban_selected(modeladmin, request, queryset):
    queryset.update(is_banned=False)
unban_selected.short_description = "Разбанить выбранных пользователей"

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'city', 'is_banned', 'ban_until','ban_button')
    list_filter = ('is_banned',)
    search_fields = ("name", "email")
    actions = [ban_selected_users, unban_selected, ban_selected]

    # Это поле будет отображать кнопку
    def ban_button(self, obj):
        if not obj.is_banned:
            return format_html(
                '<a class="button" style="background-color:red;color:white;padding:2px 6px;" href="{}">Забанить</a>',
                f'ban_toggle/{obj.id}'
            )
        else:
            # Кнопка разбанить
            return format_html(
                '<a class="button" style="background-color:green;color:white;padding:2px 6px;" href="{}">Разбанить</a>',
                f'ban_toggle/{obj.id}'
            )
    ban_button.short_description = 'Действие'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ban_toggle/<int:user_id>/', self.admin_site.admin_view(self.ban_user), name='leader-ban-toggle'),
        ]
        return custom_urls + urls

    def ban_user(self, request, user_id):
        user = Leader.objects.get(pk=user_id)
        if user.is_banned:
            user.is_banned = False
            user.ban_reason = ""
            user.ban_until = None
            self.message_user(request, f"Пользователь {user.name} разбанен!")
        else:
            user.is_banned = True
            user.ban_reason = "Админ забанил пользователя"
            user.ban_until = timezone.now() + timedelta(days=7)
            self.message_user(request, f"Пользователь {user.name} забанен!")
        user.save()
        return redirect(request.META.get('HTTP_REFERER'))


@admin.register(Candidante)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_banned', 'ban_until', "ban_button")
    list_filter = ('is_banned',)
    search_fields = ("name", "email")
    actions = [ban_selected_users, unban_selected, ban_selected]


    # Это поле будет отображать кнопку
    def ban_button(self, obj):
        if not obj.is_banned:
            return format_html(
                '<a class="button" style="background-color:red;color:white;padding:2px 6px;" href="{}">Забанить</a>',
                f'ban_toggle/{obj.id}'
            )
        else:
            # Кнопка разбанить
            return format_html(
                '<a class="button" style="background-color:green;color:white;padding:2px 6px;" href="{}">Разбанить</a>',
                f'ban_toggle/{obj.id}'
            )
    ban_button.short_description = 'Действие'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ban_toggle/<int:user_id>/', self.admin_site.admin_view(self.ban_user), name='candidante-ban-toggle'),
        ]
        return custom_urls + urls

    def ban_user(self, request, user_id):
        user = Candidante.objects.get(pk=user_id)
        if user.is_banned:
            user.is_banned = False
            user.ban_reason = ""
            user.ban_until = None
            self.message_user(request, f"Пользователь {user.name} разбанен!")
        else:
            user.is_banned = True
            user.ban_reason = "Админ забанил пользователя"
            user.ban_until = timezone.now() + timedelta(days=7)
            self.message_user(request, f"Пользователь {user.name} забанен!")
        user.save()
        return redirect(request.META.get('HTTP_REFERER'))
    
admin.site.register(Jobs)
admin.site.register(Response)