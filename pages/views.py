from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from statuses.models import Status


# Create your views here.
class HomeView(ListView):
    model = Status
    template_name = 'home.html'
