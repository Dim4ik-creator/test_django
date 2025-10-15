from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class LeaderOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('user_type') != 'leader':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class CandidateOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('user_type') != 'candidate':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
