from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from . import forms, models

class RewiewFluxView(LoginRequiredMixin, View):
    template = 'review/review_home.html'

    def get(self, request):
        return render(request, 'review/review_home.html')


class FollowView(LoginRequiredMixin, View):
    template = 'review/follows.html'
    form_class = forms.FollowForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, context=self._get_follow_context(request, form))
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            if follow.followed_user != request.user:
                follow.user = request.user
                follow.save()
        return render(request, self.template, context=self._get_follow_context(request, form))
    
    def _get_follow_context(self, request, form):
        return {
            'form': form,
            'followers': models.UserFollows.get_followers(request.user),
            'followed': models.UserFollows.get_users_followed(request.user)
        }
    

class UnfollowView(LoginRequiredMixin, View):
    template = 'review/unfollow.html'

    def get(self, request, id):
        follow = models.UserFollows.objects.get(followed_user=id, user=request.user)
        return render(request, self.template, context={'user_follow': follow.followed_user})
    
    def post(self, request, id):
        follow = models.UserFollows.objects.get(followed_user=id, user=request.user)
        follow.delete()
        return redirect('follows')