from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from . import forms, models

class RewiewFluxView(LoginRequiredMixin, View):
    template = 'review/flux.html'

    def get(self, request):
        return render(request, self.template)
    

class CreateTicketView(LoginRequiredMixin, View):
    template = 'review/ticket_add.html'

    def get(self, request):
        form = forms.AddTicketForm()
        return render(request, self.template, context={'form': form})
    
    def post(self, request):
        form = forms.AddTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
        return render(request, self.template, context={'form': form})
    

class DeleteTicketView(LoginRequiredMixin, View):

    def get(self, request, id):
        ticket = models.Ticket.objects.get(id=id)
        if ticket.user == request.user:
            ticket.delete()
        return redirect('posts')
    

class UpdateTicketView(LoginRequiredMixin, View):
    template = 'review/ticket_update.html'

    def get(self, request, id):
        ticket = models.Ticket.objects.get(id=id)
        form = forms.AddTicketForm(instance=ticket)
        return render(request, self.template, context={'form': form})
    
    def post(self, request, id):
        ticket = models.Ticket.objects.get(id=id)
        form = forms.AddTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            return redirect('posts')
        return render(request, self.template, context={'form': form})

class CreateReviewView(LoginRequiredMixin, View):
    template = 'review/review_add.html'

    def get(self, request):
        return render(request, self.template)

class PostsView(LoginRequiredMixin, View):
    template = 'review/posts.html'
    ticket_class = models.Ticket

    def get(self, request):
        tickets = self.ticket_class.objects.filter(user=request.user)
        return render(request, self.template, context={'tickets': tickets})


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