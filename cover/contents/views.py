from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import Content, FollowRelation
# Create your views here.

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user
        followees = FollowRelation.objects.filter(follower=user).values_list('followee__id', flat=True)
        lookup_user_ids = [user.id] + list(followees)
        context['contents'] = Content.objects.select_related('user').prefetch_related('image_set').filter(
            user__id__in = lookup_user_ids #이 변수는 아직 모르겠음.
        )

        return context 

