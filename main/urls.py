from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rules/', views.rules_page, name='rules'),
    path('about/', views.about_page, name='about'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('block/<int:message_id>/', views.block_sender, name='block_sender'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('message/reply/<int:message_id>/', views.reply_message, name='reply_message'),
    path('<slug:slug>/', views.public_profile, name='public_profile'),
]