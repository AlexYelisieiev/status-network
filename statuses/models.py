from time import sleep
from django.db import models
from django.urls import reverse
from django.db.models import ForeignKey
from accounts.models import CustomUser
import config
import requests


# Create your models here.
class Status(models.Model):
    text = models.TextField()
    media = models.FileField(upload_to='statuses', null=True)
    author = ForeignKey(CustomUser, on_delete=models.CASCADE,
                        related_name='status')
    is_image = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        CustomUser, blank=True, related_name='likes')
    ai_summary = models.TextField(default='', null=True, blank=True)

    def __str__(self) -> str:
        return self.text[:50]

    def get_absolute_url(self):
        return reverse('status_detail', args=[self.pk])

    def generate_ai_summary(self):
        '''Generates a short ai summary based on the Status' text'''

        api_url = config.TEXT_API_URL
        headers = {
            'Authorization': f'Bearer {config.API_TOKEN}'
        }

        payload = {
            'inputs': self.text,
        }

        while True:
            response = requests.post(api_url, headers=headers, json=payload).json()

            try:
                if 'estimated_time' in response[0]:
                    print(f"Waiting {response[0]['estimated_time']} seconds...")
                    sleep(response[0]['estimated_time'])
                    continue
            except KeyError:
                sleep(1)
                continue

            response_text = response[0]['summary_text'].replace('\n', '').replace(' .', '. ')
            self.ai_summary = response_text
            self.save(update_fields=['ai_summary'])
            print(response_text)
            break
