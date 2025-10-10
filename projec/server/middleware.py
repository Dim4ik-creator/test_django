from django.shortcuts import redirect
from .models import Leader, Candidante

class CheckBannedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_type = request.session.get('user_type')
        user_name = request.session.get('name')

        if user_type and user_name:
            if user_type == 'candidate':
                user = Candidante.objects.filter(name=user_name).first()
            else:
                user = Leader.objects.filter(name=user_name).first()
            if user and user.is_banned:
                # очистить сессию и редирект
                request.session.flush()
                return redirect('login')

        return self.get_response(request)
