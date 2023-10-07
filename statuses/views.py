from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from .models import Status
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import mimetypes


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'status_create.html'
    fields = ['text', 'media']
    login_url = 'login'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # Add the info about the media file to the post (image/video)
        form.instance.is_image = mimetypes.guess_type(
            form.instance.media.name)[0].startswith('image/')
        form.instance.author = self.request.user
        
        # Remove their previous status
        Status.objects.get(author=self.request.user).delete()
        
        return super().form_valid(form)


class StatusEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = 'login'
    template_name = 'status_edit.html'
    model = Status
    fields = ['text', 'media']

    def test_func(self) -> bool:
        return self.request.user == self.get_object().author
