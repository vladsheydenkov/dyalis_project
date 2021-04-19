from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'main_app'


urlpatterns = [
    path('', views.all_materials, name='all_materials'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',
         views.material_details, name='material_details',
         ),
    path('create/', views.create_form, name='create_form'),
    path('<int:material_id>/share/',
         views.share_material,
         name='share_material', ),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
