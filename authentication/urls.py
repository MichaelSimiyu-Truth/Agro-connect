from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.urls import path
from . import views  # Import your views from the current app

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('lock/', views.lock_screen, name='lock_screen'),
    path('unlock/', views.unlock_screen, name='unlock_screen'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
    # Supplier URLs
    path('supplier_index/', views.supplier_index, name='supplier_index'),
    path('supplier_signup/', views.supplier_signup, name='supplier_signup'),
    path('supplier_signin/', views.supplier_signin, name='supplier_signin'),
    path('supplier_signout/', views.signout, name='supplier_signout'),  # Reusing signout view
    path('supplier_activate/<uidb64>/<token>/', views.activate, name='supplier_activate'),  # Reusing activate view
    path('supplier_lock/', views.supplier_lock_screen, name='supplier_lock_screen'),
    path('supplier_unlock/', views.supplier_unlock_screen, name='supplier_unlock_screen'),
    path('supplier_password_reset/', views.supplier_password_reset_request, name='supplier_password_reset'),
    path('supplier_password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/supplier_password_reset_done.html'), name='supplier_password_reset_done'),
    path('supplier_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/supplier_password_reset_confirm.html'), name='supplier_password_reset_confirm'),
    path('supplier_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/supplier_password_reset_complete.html'), name='supplier_password_reset_complete'),
    
    # Add the edit_profile path
    path('edit_supplier/', views.edit_supplier, name='edit_supplier'),
    path('edit_farmer/', views.edit_farmer, name='edit_farmer'),
    path('farmer_index/', views.farmer_index, name='farmer_index'),
]

# Add the following line to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('lock/', views.lock_screen, name='lock_screen'),  # Correct import
    path('unlock/', views.unlock_screen, name='unlock_screen'),  # Correct import
     path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
] """

