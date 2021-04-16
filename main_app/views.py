from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from . import models

# Create your views here.


def all_materials(request):
    materials = models.Material.objects.all()
    return render(request,
                  'materials/all_materials.html',
                  {"materials": materials})


def material_details(request, year, month, day, slug):
    material = get_object_or_404(models.Material,
                                 slug=slug,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day, )
    return render(request,
                  'materials/detail.html',
                  {'material': material})
