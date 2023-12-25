from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Status
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseRedirect

import mimetypes


def generate_ai_summary_view(request: HttpRequest, status_id: int):
    chosen_status = Status.objects.get(id=status_id)

    # Check if user doesn't have permission
    if request.user != chosen_status.author:
        return HttpResponseForbidden("Not a chance!")

    # Check if entity already has an AI summary
    if chosen_status.ai_summary:
        return HttpResponseRedirect(redirect_to=reverse_lazy('home'))

    # Initiate status's AI sumary generation method
    chosen_status.generate_ai_summary()

    return HttpResponseRedirect(
        redirect_to=reverse_lazy('status_detail', kwargs={'pk': chosen_status.id}))


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

        # Remove their previous status if it exists
        if previous_status := Status.objects.filter(author=self.request.user):
            previous_status.delete()

        return super().form_valid(form)


class StatusEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''Takes either id (status' id) or user_id (user's id)'''
    login_url = 'login'
    template_name = 'status_edit.html'
    model = Status
    fields = ['text', 'media']

    # Use either status' id or user's id to find their status
    def get_object(self, queryset=None):
        if id := self.kwargs.get('id'):
            user_status = Status.objects.get(id=id)
        else:
            user_id = self.kwargs.get('user_id')
            user_status = Status.objects.get(author_id=user_id)
        return user_status
        
    def test_func(self) -> bool:
        return self.request.user == self.get_object().author

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # Reset status media type info in case it's changed 
        form.instance.is_image = mimetypes.guess_type(
            form.instance.media.name)[0].startswith('image/')
        return super().form_valid(form)


class StatusDetailView(DetailView):
    template_name = 'status_detail.html'
    model = Status


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
