from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import *
from camps.mixins import CampViewMixin

class CampInfoView(CampViewMixin, ListView):
    model = InfoCategory
    template_name = 'info.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super(CampInfoView, self).get_queryset()
        # do not show categories with 0 items
        return queryset.exclude(infoitems__isnull=True)

