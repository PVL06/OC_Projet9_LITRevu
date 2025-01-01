from django.contrib import admin

from review.models import Ticket, Review


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'time_created',
        'title',
        'response',
    )
    search_fields = ('user__username',)
    list_per_page = 50


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'time_created',
        'rating',
        'headline',
    )
    search_fields = ('user__username',)
    list_per_page = 50
