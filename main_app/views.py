from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from . import models
from . import forms
from transliterate import translit

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


def create_form(request):
    created = False
    if request.method == 'POST':
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            translit_slug = translit(new_material.title, 'ru', reversed=True)
            new_material.slug = translit_slug.replace(' ', '-')
            new_material.save()
            created = True
            return render(request,
                          'materials/create.html',
                          {'created': created, 'material': new_material})
    else:
        material_form = forms.MaterialForm()
        return render(request,
                      'materials/create.html',
                      {'created': created, 'form': material_form})


def share_material(request, material_id):
    material = get_object_or_404(models.Material,
                                 id=material_id)

    sent = False

    if request.method == 'POST':
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            material_uri = request.build_absolute_uri(
                material.get_absolute_url()
            )
            subject = '{} recommends you to review next material {}'.format(
                cd['name'],
                material.title,
            )
            body = ('{title} at {url} \n\n {name} asks you to review it.'
                    'Comment: \n\n {comment}').format(
                title=material.title,
                url=material_uri,
                name=cd['name'],
                comment=cd['comment'],
            )

            send_mail(subject,
                      body,
                      'supersiteadmin@mysite.com',
                      [cd['to_email'], ])
    else:
        form = forms.EmailMaterialForm()

    return render(request,
                  'materials/share.html',
                  {'material': material, 'form': form, 'sent': sent})
