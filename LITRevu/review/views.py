from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class RewiewFluxView(LoginRequiredMixin, View):
    template = 'review/review_home.html'

    def get(self, request):
        return render(request, 'review/review_home.html')

