from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from pathlib import Path
from django.conf import settings

from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    response = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = Path(settings.MEDIA_ROOT / str(self.image))
            image_path.unlink()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.image:
            image_size = (150, 200)
            image = Image.open(self.image)
            image.thumbnail(image_size)
            image.save(self.image.path)
        super().save(*args, **kwargs)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follow_user')

    class Meta:
        unique_together = ('user', 'followed_user', )

    @classmethod
    def get_followers(cls, user_pk):
        return cls.objects.all().filter(followed_user=user_pk)
    
    @classmethod
    def get_users_followed(cls, user_pk):
        return cls.objects.all().filter(user=user_pk)

