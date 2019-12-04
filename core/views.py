from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/index.html')
