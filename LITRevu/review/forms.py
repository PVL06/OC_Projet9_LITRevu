from django import forms

from . import models


class TicketForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 128}))
    description = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 2048}))

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Titre'


class ReviewFrom(forms.ModelForm):
    RATING_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    headline = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 128}))
    body = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 8192}))
    rating = forms.TypedChoiceField(
        widget=forms.RadioSelect,
        choices=RATING_CHOICES,
        coerce=int
        )

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = 'Note'
        self.fields['headline'].label = 'Titre'
        self.fields['body'].label = 'Commentaire'


class FollowForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user',]