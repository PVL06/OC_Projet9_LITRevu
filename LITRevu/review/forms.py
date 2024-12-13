from django import forms

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewFrom(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']


class FollowForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user',]