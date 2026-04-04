from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/messages/new/", views.api_check_new_messages, name="api_new_messages"),
    path("dashboard/analytics/", views.analytics_dashboard, name="analytics_dashboard"),
    path("rules/", views.rules_page, name="rules"),
    path("privacy/", views.privacy_page, name="privacy"),
    path("about/", views.about_page, name="about"),
    path("faq/", views.faq_page, name="faq"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("block/<int:message_id>/", views.block_sender, name="block_sender"),
    path(
        "message/favorite/<int:message_id>/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path(
        "message/react/<int:message_id>/<str:emoji>/",
        views.set_reaction,
        name="set_reaction",
    ),
    path(
        "message/reveal/<int:message_id>/",
        views.reveal_disposable_message,
        name="reveal_message",
    ),
    path(
        "message/delete/<int:message_id>/", views.delete_message, name="delete_message"
    ),
    path("message/reply/<int:message_id>/", views.reply_message, name="reply_message"),
    path("<slug:slug>/", views.public_profile, name="public_profile"),
]
