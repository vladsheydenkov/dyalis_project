from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

app_name = 'main_app'


class MyHackedPass(auth_views.PasswordResetView):
    success_url = reverse_lazy('main_app:password_reset_done')  # костыль


urlpatterns = [
    path('', views.all_materials, name='all_materials'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.material_details, name='material_details'),
    path('create/', views.create_form, name='create_form'),
    path('<int:material_id>/share/', views.share_material, name='share_material', ),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', MyHackedPass.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('main_app:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
