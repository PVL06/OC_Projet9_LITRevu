from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import CharField, Value, Q
from django.conf import settings
from itertools import chain
from pathlib import Path

from . import forms, models
from authentication.models import User


class FluxView(LoginRequiredMixin, View):
    template = 'review/flux.html'
    ticket_class = models.Ticket
    review_class = models.Review
    POST_PER_PAGE = 10

    def get(self, request):
        # Retrieve the current user's followers and the user themselves
        users_viewable = User.objects.filter(
            Q(follow_user__user=request.user) |
            Q(pk=request.user.pk)
        )
        # Fetch tickets from followed users
        tickets = self.ticket_class.objects.filter(user__in=users_viewable)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        # Fetch reviews from followed users and reviews of tickets published by followed users
        reviews = self.review_class.objects.filter(
            Q(user__in=users_viewable) |
            Q(ticket__user__in=users_viewable)
            )
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True
        )

        paginator = Paginator(posts, self.POST_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template, context={'posts': page_obj})


class PostsView(LoginRequiredMixin, View):
    template = 'review/posts.html'
    ticket_class = models.Ticket
    review_class = models.Review
    POST_PER_PAGE = 10

    def get(self, request):
        tickets = self.ticket_class.objects.filter(user=request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        reviews = self.review_class.objects.filter(user=request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True
        )

        paginator = Paginator(posts, self.POST_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template, context={'posts': page_obj})


class CreateTicketView(LoginRequiredMixin, View):
    template = 'review/ticket_add.html'
    form_class = forms.TicketForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')

        return render(request, self.template, context={'form': form})


class CreateCompleteReviewView(LoginRequiredMixin, View):
    template = 'review/review_complete_add.html'
    ticket_form_class = forms.TicketForm
    review_form_class = forms.ReviewFrom

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
            ticket.response = True
            review = review_form.save(commit=False)
            review.ticket = ticket
            ticket.user = review.user = request.user
            ticket.save()
            review.save()
            return redirect('flux')

        context = {
            'ticket_form': ticket_form,
            'review_form': review_form
        }
        return render(request, self.template, context=context)


class ResponseToTicketView(LoginRequiredMixin, View):
    ticket_template = 'review/ticket_response.html'
    review_form_class = forms.ReviewFrom
    ticket_class = models.Ticket

    def get(self, request, id):
        ticket = get_object_or_404(self.ticket_class, id=id)
        form = self.review_form_class()
        return render(request, self.ticket_template, context={'form': form, 'post': ticket})

    def post(self, request, id):
        ticket = get_object_or_404(self.ticket_class, id=id)
        form = self.review_form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            ticket.response = True
            ticket.save()
            return redirect('flux')

        return render(request, self.ticket_template, context={'form': form, 'post': ticket})


class UpdateContentView(LoginRequiredMixin, View):
    ticket_template = 'review/ticket_update.html'
    review_template = 'review/review_update.html'
    ticket_form_class = forms.TicketForm
    review_form_class = forms.ReviewFrom
    ticket_class = models.Ticket
    review_class = models.Review

    def get(self, request, content_type, id):
        if content_type == 'ticket':
            ticket = get_object_or_404(self.ticket_class, id=id)
            if ticket.user != request.user:
                return redirect('flux')
            # Remove the image from the model to control it in the template
            ticket_img = ticket.image if ticket.image else ''
            ticket.image = ''
            form = self.ticket_form_class(instance=ticket)
            return render(request, self.ticket_template, context={'form': form, 'img': ticket_img})

        elif content_type == 'review':
            review = get_object_or_404(self.review_class, id=id)
            if review.user != request.user:
                return redirect('flux')
            form = self.review_form_class(instance=review)
            return render(request, self.review_template, context={'form': form, 'post': review.ticket})

    def post(self, request, content_type, id):
        if content_type == 'ticket':
            ticket = get_object_or_404(self.ticket_class, id=id)
            last_image = str(ticket.image)
            form = self.ticket_form_class(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                if ticket.user == request.user:
                    ticket = form.save()
                    # Delete the image file if modified
                    if last_image != ticket.image:
                        image_path = Path(settings.MEDIA_ROOT / last_image)
                        image_path.unlink()
                return redirect('posts')

        elif content_type == 'review':
            review = get_object_or_404(self.review_class, id=id)
            form = self.review_form_class(request.POST, instance=review)
            if form.is_valid():
                if review.user == request.user:
                    review = form.save()
                return redirect('posts')

        return render(request, self.ticket_template, context={'form': form})


class DeleteContentView(LoginRequiredMixin, View):
    template = 'review/delete_post.html'
    ticket_class = models.Ticket
    review_class = models.Review

    def get(self, request, content_type, id):
        if content_type == 'ticket':
            ticket = get_object_or_404(self.ticket_class, id=id)
            if ticket.user == request.user:
                return render(request, self.template, context={'type': 'ticket', 'post': ticket})

        if content_type == 'review':
            review = get_object_or_404(self.review_class, id=id)
            if review.user == request.user:
                return render(request, self.template, context={'type': 'review', 'post': review})

        return redirect('posts')

    def post(self, request, content_type, id):
        if content_type == 'ticket':
            ticket = get_object_or_404(self.ticket_class, id=id)
            if ticket.user == request.user:
                ticket.delete()

        if content_type == 'review':
            review = get_object_or_404(self.review_class, id=id)
            if review.user == request.user:
                ticket = get_object_or_404(self.ticket_class, id=review.ticket.id)
                ticket.response = False
                ticket.save()
                review.delete()

        return redirect('posts')


class FollowView(LoginRequiredMixin, View):
    template = 'review/follows.html'
    follow_form_class = forms.FollowForm
    follow_class = models.UserFollows

    def get(self, request):
        form = self.follow_form_class()
        # Select unfollowed users, excluding the superuser and the current user
        no_following = User.objects.exclude(
            Q(follow_user__user=request.user) |
            Q(pk=request.user.pk) |
            Q(is_superuser=True)
            )
        form.fields['followed_user'].queryset = no_following
        return render(request, self.template, context=self._get_follow_context(request, form))

    def post(self, request):
        form = self.follow_form_class(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            if follow.followed_user != request.user:
                follow.user = request.user
                follow.save()
        return redirect('follows')

    def _get_follow_context(self, request, form):
        return {
            'form': form,
            'followers': self.follow_class.get_followers(request.user),
            'followed': self.follow_class.get_users_followed(request.user)
        }


class UnfollowView(LoginRequiredMixin, View):
    template = 'review/unfollow.html'
    follow_class = models.UserFollows

    def get(self, request, id):
        follow = self.follow_class.objects.get(followed_user=id, user=request.user)
        return render(request, self.template, context={'user_follow': follow.followed_user})

    def post(self, request, id):
        follow = self.follow_class.objects.get(followed_user=id, user=request.user)
        follow.delete()
        return redirect('follows')
