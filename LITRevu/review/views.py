from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from . import forms, models

class RewiewFluxView(LoginRequiredMixin, View):
    template = 'review/flux.html'

    def get(self, request):
        return render(request, self.template)
    

class CreateTicketView(LoginRequiredMixin, View):
    template = 'review/ticket_add.html'
    form_class = forms.AddTicketForm

    def get(self, request):
        form = self.form_class()
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
        ticket = get_object_or_404(models.Ticket, id=id)
        if ticket.user == request.user:
            ticket.delete()
        return redirect('posts')
    

class UpdateTicketView(LoginRequiredMixin, View):
    template = 'review/ticket_update.html'
    form_class = forms.AddTicketForm

    def get(self, request, id):
        ticket = get_object_or_404(models.Ticket, id=id)
        form = self.form_class(instance=ticket)
        return render(request, self.template, context={'form': form})
    
    def post(self, request, id):
        ticket = get_object_or_404(models.Ticket, id=id)
        form = self.form_class(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect('posts')
        return render(request, self.template, context={'form': form})

class CreateReviewView(LoginRequiredMixin, View):
    template = 'review/review_add.html'
    ticket_form_class = forms.AddTicketForm
    review_form_class = forms.AddReviewFrom

    def get(self, request):
        ticket_form = self.ticket_form_class()
        review_form = self.review_form_class()
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form
        }
        return render(request, self.template, context=context)
    
    def post(self, request):
        ticket_form = self.ticket_form_class(request.POST, request.FILES)
        review_form = self.review_form_class(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            review = review_form.save(commit=False)
            review.ticket = ticket
            ticket.user = request.user
            review.user = request.user
            ticket.save()
            review.save()
            return redirect('flux')
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form
        }
        return render(request, self.template, context=context)
    

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, id):
        review = models.Review.objects.get(id=id)
        review.delete()
        return redirect('posts')

class PostsView(LoginRequiredMixin, View):
    template = 'review/posts.html'
    ticket_class = models.Ticket
    review_class = models.Review

    def get(self, request):
        tickets = self.ticket_class.objects.filter(user=request.user)
        reviews = self.review_class.objects.filter(user=request.user)
        context = {
            'tickets': tickets,
            'reviews': reviews
        }
        return render(request, self.template, context=context)


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