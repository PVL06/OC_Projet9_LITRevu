from django.contrib import admin
from authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'last_login',
        'date_joined',
        'ticket_count',
        'review_count',
        'is_superuser',
    )
    search_fields = ('username',)
    list_per_page = 50
