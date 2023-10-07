from django.db import models
from django.urls import reverse
from django.db.models import ForeignKey

from accounts.models import CustomUser


# Create your models here.
class Status(models.Model):
    text = models.TextField()
    media = models.FileField(upload_to='statuses', null=True)
    author = ForeignKey(CustomUser, on_delete=models.CASCADE,
                        related_name='status')
    is_image = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text[:50]

    def get_absolute_url(self):
        return reverse('home')
