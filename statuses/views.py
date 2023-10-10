from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Status

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

    def get_object(self, queryset=None):
        if id := self.kwargs.get('id'):
            user_status = Status.objects.get(id=id)
        else:
            user_id = self.kwargs.get('user_id')
            print('user_id')
            user_status = Status.objects.get(author_id=user_id)
        return user_status
        
    def test_func(self) -> bool:
        return self.request.user == self.get_object().author


class StatusLikeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, status_id):
        status = Status.objects.get(id=status_id)
        user = request.user
        if not status.likes.filter(id=user.id).exists():
            status.likes.add(user)
        else:
            status.likes.remove(user)
        return HttpResponseRedirect(reverse('home'))

    def post(self, request, status_id):
        status = Status.objects.get(id=status_id)
        user = request.user
        if not status.likes.filter(id=user.id).exists():
            status.likes.add(user)
        else:
            status.likes.remove(user)
        return HttpResponseRedirect(reverse('home'))
