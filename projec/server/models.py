from django.db import models
from django.utils import timezone
from datetime import timedelta


class Leader(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=50, blank=False, unique=True)
    company = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=128, blank=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True, verbose_name="Причина блокировки")
    ban_until = models.DateTimeField(blank=True, null=True, verbose_name="Дата окончания блокировки")
    

    def ban(self, reason="", days=None):
        """Блокировка пользователя с причиной и сроком"""
        self.is_banned = True
        self.ban_reason = reason
        if days:
            self.ban_until = timezone.now() + timedelta(days=days)
        self.save()

    def unban(self):
        """Снять блокировку"""
        self.is_banned = False
        self.ban_reason = None
        self.ban_until = None
        self.save()

    def is_currently_banned(self):
        """Проверяет, активен ли бан"""
        if not self.is_banned:
            return False
        if self.ban_until and self.ban_until < timezone.now():
            # Бан истёк — снимаем
            self.unban()
            return False
        return True

    def __str__(self):
        return self.name
    

class Candidante(models.Model):
    name = models.CharField(max_length=50, blank=False)
    bio = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=False,  unique=True)
    password = models.CharField(max_length=128, blank=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True, verbose_name="Причина блокировки")
    ban_until = models.DateTimeField(blank=True, null=True, verbose_name="Дата окончания блокировки")


    def ban(self, reason="", days=None):
        """Блокировка пользователя с причиной и сроком"""
        self.is_banned = True
        self.ban_reason = reason
        if days:
            self.ban_until = timezone.now() + timedelta(days=days)
        self.save()

    def unban(self):
        """Снять блокировку"""
        self.is_banned = False
        self.ban_reason = None
        self.ban_until = None
        self.save()

    def is_currently_banned(self):
        """Проверяет, активен ли бан"""
        if not self.is_banned:
            return False
        if self.ban_until and self.ban_until < timezone.now():
            # Бан истёк — снимаем
            self.unban()
            return False
        return True


    def __str__(self):
        return self.name

class Jobs(models.Model):
    leader = models.ForeignKey(Leader, on_delete=models.CASCADE, related_name='jobs', null=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    location = models.CharField(max_length=255, blank=False)
    salary = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Response(models.Model):
    candidate = models.ForeignKey(Candidante, on_delete=models.CASCADE, related_name="responses")
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name="responses")
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')  # чтобы нельзя было откликнуться дважды

    def __str__(self):
        return f"{self.candidate.name} → {self.job.title}"